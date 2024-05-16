from urllib.request import Request
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.shortcuts import get_object_or_404, Http404
from django.db import transaction, IntegrityError
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from lms.api.business import create_notify_request, check_payment_life_cycle_is_completed
from lms.api.decorators import api_response, with_scart_from_request
from lms.coworkers.cdek import Cdek
from lms.coworkers.dadata import DaData
from lms.coworkers.postru import PostRu
from lms.models import Product, AvailableSize, Parameter, Order, OrderItem, City, AboutItem
from lms.api.serializers import ProductSerializer, ProductDetailSerializer, AboutItemSerializer
from lms.utils import D6Y, deep_unquote
from customerinfo.customerinfo import CustomerInfo, with_actual_scart_records_and_price
from lms.coworkers.yookassa import Yookassa
import logging
import re


class ProductListView(generics.ListAPIView):
    queryset = Product.published.all()
    serializer_class = ProductSerializer


class ProductListPageView(generics.ListAPIView):
    serializer_class = ProductSerializer
    default_order = 'novelties-first'
    ordering = {
        default_order: ("Порядок: по умолчанию", lambda q: q.order_by('-published_at')),
        'price-asc': ("Цена: по возрастанию", lambda q: q.order_by('actual_price')),
        'price-dsc': ("Цена: по убыванию", lambda q: q.order_by('-actual_price')),
        'title-asc': ("Название: А-Я", lambda q: q.order_by('title')),
        'title-dsc': ("Название: Я-А", lambda q: q.order_by('-title')),
        'bestsellers': ("Бестселлеры", lambda q: q.order_by('-sales_quantity')),
    }

    def __init__(self):
        super().__init__()
        self.order = ProductListPageView.default_order
        self.filter = None
        self.pgs = 10
        self.pgn = 1

    def validate(self):
        return self.order in ProductListPageView.ordering and self.pgs > 0 and self.pgn > 0

    def get(self, *args, **kwargs):
        try:
            self.order = kwargs['order']
            self.filter = deep_unquote(kwargs['filter']) if 'filter' in kwargs else None
            self.pgs = abs(int(kwargs['pgs']))
            self.pgn = abs(int(kwargs['pgn']))
            if not self.validate():
                raise Http404()
        except (KeyError, ValueError) as e:
            raise Http404(e)
        result = super().get(*args, **kwargs)
        result.data = {
            'total-count': self.queryset().count(),
            'data': result.data,
        }
        return result

    def queryset(self):
        if self.filter:
            try:
                if not re.match(settings.SEARCH_INPUT_RGX, self.filter):
                    raise re.error(self.filter)
                re.compile(self.filter)
                rx = self.filter
            except re.error:
                rx = '^$'
            return Product.published.filter(title__iregex=rx)
        return Product.published.all()

    def page(self, q):
        a = self.pgs * (self.pgn - 1)
        b = a + self.pgs
        return q[a:b]

    def get_queryset(self):
        return self.page(ProductListPageView.ordering[self.order][1](self.queryset())) if self.validate() else self.queryset()


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.published.all()
    serializer_class = ProductDetailSerializer


class ProductIsFavoriteView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def get(request, ppk, _=None):
        info = CustomerInfo(request)
        return {'favorite': ppk in info.favorites}


class ProductLikeSetView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, ppk, like: int, _=None):
        info = CustomerInfo(request)
        if like:
            info.add_favorite(ppk)
        else:
            info.remove_favorite(ppk)
        return {'ppk': ppk, 'like': like}


class ProductLikeToggleView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, ppk, _=None):
        info = CustomerInfo(request)
        if ppk in info.favorites:
            info.remove_favorite(ppk)
            return {'ppk': ppk, 'like': 0}
        else:
            info.add_favorite(ppk)
            return {'ppk': ppk, 'like': 1}


class ProductSizeQuantityView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):
        data = request.data
        try:
            prod = Product.objects.get(pk=data["ppk"])
            size = prod.sizes.get(pk=data["size"])
            return {
                "quantity": size.quantity
            }
        except (Product.DoesNotExist, AvailableSize.DoesNotExist, KeyError):
            return "Not found"


class SetLocationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):
        data = request.data
        try:
            location = {
                "latitude": float(data["latitude"]),
                "longitude": float(data["longitude"]),
                "accuracy": float(data["accuracy"]),
            }
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        CustomerInfo(request).location = location
        return location


class GetCustomerInfoView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, flags, _=None):
        info = CustomerInfo(request)
        items = {
            0b000000001: lambda: {"name": info.short_name, "first_name": info.first_name, "last_name": info.last_name},
            0b000000010: lambda: {"phone": info.phone},
            0b000000100: lambda: {"email": info.email},
            0b000001000: lambda: {"address": info.address},
            0b000010000: lambda: {"favorites": info.favorites},
            0b000100000: lambda: {"scart": info.scart},
            0b001000000: lambda: {"location": info.location},
        }
        result = {}
        for mask in items.keys():
            if flags & mask:
                result |= items[mask]()
        return result


class NotifyMeForDeliveryView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):
        cu_data = request.data
        try:
            phone, email, ppk = escape(cu_data['phone']), escape(cu_data['email']), escape(cu_data['ppk'])
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        if ppk and (email or phone):
            create_notify_request(email, phone, ppk, CustomerInfo(request))
            return {'success': True}
        return Parameter.value_of('message_unable_notify', 'Почта или телефон должны быть указаны')


@with_actual_scart_records_and_price
def get_current_scart(rq: Request, scart):
    def product(p: Product):
        return {
            'article': p.article,
            'title': p.title,
            'description': p.description,
            'novelty': p.novelty,
            'actual_price': p.actual_price.amount,
            'old_price': p.old_price.amount if p.old_price else None,
            'in_stock': p.in_stock,
            'primary_image': p.primary_image.image.url,
        }

    def size(s: AvailableSize):
        return {
            'id': s.id,
            'size': s.size,
        }

    return {
        'price': scart['price'],
        'weight': scart['weight'],
        'records': [{
            'product': product(r['product']),
            'size': size(r['size']),
            'quantity': r['quantity'],
        } for r in scart['records']]}


class ProductToSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):
        data = request.data
        try:
            ppk, size_id, quantity = data['ppk'], int(data['size_id']), int(data['quantity'])
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        try:
            product = get_object_or_404(Product.published, pk=ppk)
        except Http404:
            return Parameter.value_of('message_product_not_found_by_article', 'Не удалось найти товар с артикулом %s') % (ppk,)
        try:
            size = get_object_or_404(AvailableSize, id=size_id)
        except Http404:
            return Parameter.value_of('message_size_not_found_by_id', 'Не удалось найти нужный размер')
        if not product.sizes.filter(id=size_id).exists():
            return Parameter.value_of('message_product_has_no_size', 'Для товара %s недоступен размер %s') % (product, size)
        info = CustomerInfo(request)
        return {
            'product': str(product),
            'size': str(size),
            'quantity': info.add_to_scart(ppk, size.size, quantity),
            'scart': get_current_scart(request),
        } if info.add_to_scart(ppk, size.size, quantity, True) <= size.quantity or quantity < 0 \
            else Parameter.value_of('message_overkill', 'Извините, достигнут лимит. Это максимально возможное количество товаров в наличии.')


class KillProductInSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):
        data = request.data
        try:
            ppk, size = data['ppk'], data['size']
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        data = CustomerInfo(request).remove_from_scart(ppk, size)
        return {
            'ppk': data['ppk'],
            'size': data['size'],
            'quantity': data['quantity'],
            'scart': get_current_scart(request),
        } if data else Parameter.value_of('message_product_not_found_in_shopping_cart', 'Товар с артикулом %s и размером %s не найден в корзине') % (ppk, size)


class GetSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def get(request, _=None):
        return {
            'scart': get_current_scart(request),
        }


class CheckoutSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    @with_actual_scart_records_and_price
    def post(request, scart, _=None):
        data = {k: escape(v) for k, v in request.data.items()}
        try:
            d6y_service, \
                cu_first_name, \
                cu_last_name, \
                cu_phone, \
                cu_country, \
                cu_city_uuid, \
                cu_city, \
                cu_street, \
                cu_building, \
                cu_entrance, \
                cu_floor, \
                cu_apartment, \
                cu_fullname, \
                cu_confirm = D6Y(data["delivery"]), \
                data["cu_first_name"], \
                data["cu_last_name"], \
                data["cu_phone"], \
                data["cu_country"] if "cu_country" in data else "RU", \
                data["cu_city_uuid"], \
                data["cu_city"], \
                data["cu_street"], \
                data["cu_building"], \
                data["cu_entrance"], \
                data["cu_floor"], \
                data["cu_apartment"], \
                data["cu_fullname"], \
                data["cu_confirm"]
        except (TypeError, KeyError):
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        if d6y_service and \
                cu_first_name and \
                cu_last_name and \
                cu_phone and \
                cu_country and \
                cu_city_uuid and \
                cu_city and \
                cu_street and \
                cu_building and \
                cu_entrance and \
                cu_floor and \
                cu_apartment and \
                cu_fullname and \
                cu_confirm:
            if cu_confirm != "True":
                return Parameter.value_of('message_you_must_agree_pp', 'Необходимо согласиться с политикой конфиденциальности')
            records, price = scart["records"], scart["price"]
            if not records:
                return Parameter.value_of('message_shopping_cart_empty', 'Корзина пуста. Добавьте в корзину хотя бы один товар!')
            try:
                city = City.objects.get(pk=cu_city_uuid)
            except (ValidationError, City.DoesNotExist):
                return "Пункт назначения заказа неверен."
            d6y_cost, d6y_time, error = {D6Y.CD: Cdek(), D6Y.PR: PostRu()}[d6y_service].delivery_cost(city.code, scart["weight"], price=price)
            if error:
                return error
            try:
                with transaction.atomic():
                    order = Order(delivery_service=d6y_service,
                                  delivery_cost=d6y_cost,
                                  city=city,
                                  cu_first_name=cu_first_name,
                                  cu_last_name=cu_last_name,
                                  cu_phone=cu_phone,
                                  cu_country=cu_country,
                                  cu_city_uuid=city.city_uuid,
                                  cu_city=cu_city,
                                  cu_city_region=city.region.region,
                                  cu_city_subregion=city.sub_region,
                                  cu_street=cu_street,
                                  cu_building=cu_building,
                                  cu_entrance=cu_entrance,
                                  cu_floor=cu_floor,
                                  cu_apartment=cu_apartment,
                                  cu_fullname=cu_fullname,
                                  cu_confirm=True)
                    for rec in records:
                        product = rec["product"]
                        size = rec["size"]
                        quantity = rec["quantity"]
                        item = OrderItem(order=order,
                                         product=product,
                                         ppk=product.article,
                                         title=str(product),
                                         size=size.size,
                                         quantity=quantity,
                                         price=product.actual_price,
                                         weight=product.weight)
                        item.save()
                        product.sales_quantity += quantity
                        product.save()
                        size.quantity -= quantity  # or IntegrityError on constraint
                        size.save()
                    order.save()
                    payment_id, payment_url, error = Yookassa().create_payment(order, price + Decimal(d6y_cost))
                    if error:
                        raise ValueError(error)  # breaks transaction!
                    order.payment_id = payment_id
                    order.save()
            except IntegrityError:
                return Parameter.value_of("message_overkill_in_shopping_cart", "Указанное количество товара недоступно. Возможно, кто-то уже купил его, пока Вы оформляли заказ.")
            except ValueError as exc:
                return exc.args[0]
            else:
                info = CustomerInfo(request)  # -- update session info --
                info.clear_scart()
                info.payment_id = payment_id
                info.first_name = cu_first_name
                info.last_name = cu_last_name
                info.phone = cu_phone or info.phone
                info.address = {
                    "country": cu_country,
                    "city_uuid": cu_city_uuid,
                    "city": cu_city,
                    "street": cu_street,
                    "building": cu_building,
                    "entrance": cu_entrance,
                    "floor": cu_floor,
                    "apartment": cu_apartment,
                    "fullname": cu_fullname,
                }
                return {'redirect': payment_url}
        return Parameter.value_of('message_wrong_input', 'Пожалуйста, правильно введите данные')


# -- Service --

class Service_EstimateSCart_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    @with_scart_from_request('scart')
    def post(request, scart, errors, _=None):

        def err(typ, text, reason):
            errors.append({
                "error-type": typ,
                "error-text": text,
                "error-reason": reason,
            })

        data = request.data
        result = {
            'price': scart['price'],
            'old_price': scart['old_price'],
            'weight': scart['weight'],
            'errors': errors,
        }
        if 'cu_city_uuid' in data:
            try:
                city_uuid = str(data['cu_city_uuid'])
                try:
                    city = City.objects.get(pk=city_uuid)
                except ValidationError:
                    return Parameter.value_of('message_wrong_uuid', 'Некорректный UUID')
                except City.DoesNotExist:
                    err("item-does-not-exist", "Пункт назначения не найден", {'cu_city_uuid': city_uuid})
                else:
                    cd_d6y_cost, cd_d6y_time, cd_error = Cdek().delivery_cost(city.code, scart["weight"], price=scart['price'])
                    pr_d6y_cost, pr_d6y_time, pr_error = PostRu().delivery_cost(city.code, scart["weight"], price=scart['price'])
                    result[D6Y.CD] = {'cost': cd_d6y_cost, 'days': cd_d6y_time, 'error': cd_error}
                    result[D6Y.PR] = {'cost': pr_d6y_cost, 'days': pr_d6y_time, 'error': pr_error}
            except (TypeError, KeyError):
                return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
            except ValueError:
                return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        return result


class Service_Checkout_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    @with_scart_from_request('scart')
    def post(request, scart, errors, _=None):
        for e in errors:
            return e["error-text"]
        data = {k: escape(v) for k, v in request.data.items()}
        try:
            d6y_service, \
                cu_first_name, \
                cu_last_name, \
                cu_phone, \
                cu_country, \
                cu_city_uuid, \
                cu_city, \
                cu_street, \
                cu_building, \
                cu_entrance, \
                cu_floor, \
                cu_apartment, \
                cu_fullname, \
                cu_confirm = D6Y(data["delivery"]), \
                data["cu_first_name"], \
                data["cu_last_name"], \
                data["cu_phone"], \
                data["cu_country"] if "cu_country" in data else "RU", \
                data["cu_city_uuid"], \
                data["cu_city"], \
                data["cu_street"], \
                data["cu_building"], \
                data["cu_entrance"], \
                data["cu_floor"], \
                data["cu_apartment"], \
                data["cu_fullname"], \
                data["cu_confirm"]
        except (TypeError, KeyError):
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        if d6y_service and \
                cu_first_name and \
                cu_last_name and \
                cu_phone and \
                cu_country and \
                cu_city_uuid and \
                cu_city and \
                cu_street and \
                cu_building and \
                cu_entrance and \
                cu_floor and \
                cu_apartment and \
                cu_fullname and \
                cu_confirm:
            if cu_confirm != "True":
                return Parameter.value_of('message_you_must_agree_pp', 'Необходимо согласиться с политикой конфиденциальности')
            records, price = scart["records"], scart["price"]
            if not records:
                return Parameter.value_of('message_shopping_cart_empty', 'Корзина пуста. Добавьте в корзину хотя бы один товар!')
            try:
                city = City.objects.get(pk=cu_city_uuid)
            except (ValidationError, City.DoesNotExist):
                return "Пункт назначения заказа неверен."
            d6y_cost, d6y_time, error = {D6Y.CD: Cdek(), D6Y.PR: PostRu()}[d6y_service].delivery_cost(city.code, scart["weight"], price=price)
            if error:
                return error
            try:
                with transaction.atomic():
                    order = Order(delivery_service=d6y_service,
                                  delivery_cost=d6y_cost,
                                  city=city,
                                  cu_first_name=cu_first_name,
                                  cu_last_name=cu_last_name,
                                  cu_phone=cu_phone,
                                  cu_country=cu_country,
                                  cu_city_uuid=city.city_uuid,
                                  cu_city=cu_city,
                                  cu_city_region=city.region.region,
                                  cu_city_subregion=city.sub_region,
                                  cu_street=cu_street,
                                  cu_building=cu_building,
                                  cu_entrance=cu_entrance,
                                  cu_floor=cu_floor,
                                  cu_apartment=cu_apartment,
                                  cu_fullname=cu_fullname,
                                  cu_confirm=True)
                    for rec in records:
                        product = rec["product"]
                        size = rec["size"]
                        quantity = rec["quantity"]
                        item = OrderItem(order=order,
                                         product=product,
                                         ppk=product.article,
                                         title=str(product),
                                         size=size.size,
                                         quantity=quantity,
                                         price=product.actual_price,
                                         weight=product.weight)
                        item.save()
                        product.sales_quantity += quantity
                        product.save()
                        size.quantity -= quantity  # or IntegrityError on constraint
                        size.save()
                    order.save()
                    payment_id, payment_url, error = Yookassa().create_payment(order, price + Decimal(d6y_cost))
                    if error:
                        raise ValueError(error)  # breaks transaction!
                    order.payment_id = payment_id
                    order.save()
            except IntegrityError:
                return Parameter.value_of("message_overkill_in_shopping_cart", "Указанное количество товара недоступно. Возможно, кто-то уже купил его, пока Вы оформляли заказ.")
            except ValueError as exc:
                return exc.args[0]
            else:
                return {
                    'payment_id': order.payment_id,
                    'redirect': payment_url
                }
        return Parameter.value_of('message_wrong_input', 'Пожалуйста, правильно введите данные')


class Service_CityList_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def get(request, filter: str):
        filter = deep_unquote(filter)
        try:
            if not re.match(settings.SEARCH_INPUT_RGX, filter):
                raise re.error(filter)
            re.compile(filter)
            rx = f"^{filter}"
        except re.error:
            rx = '^$'
        result = [{
            "uuid": c.city_uuid,
            "city": c.city,
            "region": c.region.region if c.region else None,
            "sub-region": c.sub_region,
        } for c in City.objects.filter(city__iregex=rx).order_by('city')]
        return {
            'cities': result,
        }


class Service_Hints_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def get(request, city_uuid: str, street: str, building: str = None):
        city_uuid = deep_unquote(city_uuid)
        try:
            city = City.objects.get(pk=city_uuid)
        except (ValidationError, City.DoesNotExist):
            return "UUID города указан неправильно"
        street = deep_unquote(street) if street else None
        building = deep_unquote(building) if building else None
        if not street:
            return "Не указана улица"
        flag = not building
        dadata = DaData()
        suggestions = (dadata.suggest_address(
            query=f"{city.region.region}, {city.city}, {street}",
            count=5,
            from_bound={"value": "street"},
            to_bound={"value": "street"}
        ) if flag else dadata.suggest_address(
            query=f"{city.region.region}, {city.city}, {street}, {building}",
            count=10,
            from_bound={"value": "house"},
            to_bound={"value": "house"}
        ))["suggestions"]
        result = list(
            {x['data']['street_with_type'] for x in suggestions if 'data' in x and 'street_with_type' in x['data']
             } if flag else {x['data']['house'] for x in suggestions if 'data' in x and 'house' in x['data']})
        result.sort()
        return {
            "streets" if flag else "buildings": result
        }


class Service_PaymentStatus_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def get(request, payment_id: str):
        payment_id = deep_unquote(payment_id)
        status, payment = Yookassa().get_payment_status(payment_id)
        return {
            'status': status,
            'payment': payment,
        }


class Service_AboutItemList_View(generics.ListAPIView):
    queryset = AboutItem.objects.all()
    serializer_class = AboutItemSerializer

    @api_response
    def get(self, *args, **kwargs):
        return {
            "items": super().get(*args, **kwargs).data
        }


class Yookassa_PaymentsWebHook_View(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, _=None):  # Проверялось только локально!
        data = request.data
        logging.info(f"Получено уведомление: {data}")
        try:
            if data["type"] == "notification" and data["event"].startswith("payment."):
                payment = data["object"]
                payment_id = payment["id"]
                payment_status = Yookassa.PaymentStatus(payment["status"])
                check_payment_life_cycle_is_completed(payment_id, payment_status, payment)
        except (KeyError, ValueError):
            logging.warning(f"Ошибка в структуре уведомления: {data}")
        return {}
