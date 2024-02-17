from django.utils.html import escape
from django.shortcuts import get_object_or_404, Http404
from django.db import transaction, IntegrityError
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics

from lms.api.business import create_notify_request
from lms.api.decorators import api_response
from lms.coworkers.cdek import Cdek
from lms.coworkers.postru import PostRu
from lms.models import Product, AvailableSize, Parameter, Order, OrderItem, City
from lms.api.serializers import ProductSerializer
from lms.utils import D6Y
from customerinfo.customerinfo import CustomerInfo, with_actual_scart_records_and_price
from lms.coworkers.yookassa import Yookassa
import logging


class ProductListView(generics.ListAPIView):
    queryset = Product.published.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.published.all()
    serializer_class = ProductSerializer


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


class GetCustomerInfoView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    def post(request, flags, _=None):
        info = CustomerInfo(request)
        items = {
            0b000000001: lambda: {"name": info.name},
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
            name, phone, email, ppk = escape(cu_data['name']), escape(cu_data['phone']), escape(cu_data['email']), escape(cu_data['ppk'])
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        if name and ppk and (email or phone):
            create_notify_request(email, name, phone, ppk, CustomerInfo(request))
            return {'success': True}
        return Parameter.value_of('message_unable_notify', 'Имя, а также почта или телефон должны быть указаны')


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
            'quantity': info.add_to_scart(ppk, size.size, quantity)
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
            'quantity': data['quantity']
        } if data else Parameter.value_of('message_product_not_found_in_shopping_cart', 'Товар с артикулом %s и размером %s не найден в корзине') % (ppk, size)


class CheckoutSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @api_response
    @with_actual_scart_records_and_price
    def post(request, scart, _=None):
        data = {k: escape(v) for k, v in request.data.items()}
        try:
            d6y_service, \
                cu_name, \
                cu_phone, \
                cu_email, \
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
                data["cu_name"], \
                data["cu_phone"], \
                data["cu_email"], \
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
        except KeyError:
            return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
        except ValueError:
            return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
        if d6y_service and \
                cu_name and \
                (cu_phone or cu_email) and \
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
            except City.DoesNotExist:
                return "Пункт назначения заказа неверен."
            d6y_cost, d6y_time, error = {D6Y.CD: Cdek(), D6Y.PR: PostRu()}[d6y_service].delivery_cost(
                city.code,
                scart["weight"],
                city=city.city_full,
                street=cu_street,
                building=cu_building,
                price=price)
            if error:
                return error
            try:
                with transaction.atomic():
                    order = Order(delivery_service=d6y_service,
                                  delivery_cost=d6y_cost,
                                  city=city,
                                  cu_name=cu_name,
                                  cu_phone=cu_phone,
                                  cu_email=cu_email,
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
                info.name = cu_name
                info.phone = cu_phone or info.phone
                info.email = cu_email or info.email
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


class YoPaymentsWebHookView(APIView):
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
                if payment_status in Yookassa.final_payment_statuses:
                    Yookassa().payment_life_cycle_is_completed(payment_id, payment_status, payment)
        except (KeyError, ValueError):
            logging.warning(f"Ошибка в структуре уведомления: {data}")
        return {}


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


