from django.utils.html import escape
from django.shortcuts import get_object_or_404, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from lms.models import Product, NotificationRequest, AvailableSize, Parameter
from lms.api.serializers import ProductSerializer
from lms.utils import send_message_via_telegram
from customerinfo.customerinfo import CustomerInfo


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLikeSetView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, ppk, like: int, _=None):
        info = CustomerInfo(request)
        if like:
            info.add_favorite(ppk)
        else:
            info.remove_favorite(ppk)
        return Response({
            'ppk': ppk,
            'like': like
        })


class ProductLikeToggleView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, ppk, _=None):
        info = CustomerInfo(request)
        if ppk in info.favorites:
            info.remove_favorite(ppk)
            return Response({
                'ppk': ppk,
                'like': 0
            })
        else:
            info.add_favorite(ppk)
            return Response({
                'ppk': ppk,
                'like': 1
            })


class GetCustomerInfoView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, flags, _=None):
        info = CustomerInfo(request)
        items = {
            0b000000001: lambda: {"name": info.name},
            0b000000010: lambda: {"phone": info.phone},
            0b000000100: lambda: {"email": info.email},
            0b000001000: lambda: {"address": info.address},
            0b000010000: lambda: {"favorites": info.favorites},
            0b000100000: lambda: {"scart": info.scart},
        }
        result = {}
        for mask in items.keys():
            if flags & mask:
                result |= items[mask]()
        return Response(result)


class NotifyMeForDeliveryView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, _=None):
        cui = request.data
        try:
            name, phone, email, ppk = escape(cui['name']), escape(cui['phone']), escape(cui['email']), escape(cui['ppk'])
        except KeyError:
            return Response({'ok': False})  # TODO -- rename 'ok' to 'success' --
        if name and ppk and (email or phone):
            nrq = NotificationRequest(name=name, phone=phone, email=email, ppk=ppk)
            nrq.save()
            send_message_via_telegram(str(nrq))
            info = CustomerInfo(request)
            info.name = name
            info.phone = phone or info.phone
            info.email = email or info.email
            return Response({
                'ok': True
            })
        return Response({
            'ok': False
        })


class ProductToSCartView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, _=None):
        info = CustomerInfo(request)
        rec = request.data
        try:
            ppk, size_id, quantity = rec['ppk'], int(rec['size_id']), int(rec['quantity'])
        except KeyError:
            return Response({
                'success': False,
                'why': Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
            })
        except ValueError:
            return Response({
                'success': False,
                'why': Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
            })
        try:
            product = get_object_or_404(Product, article=ppk)
        except Http404:
            return Response({
                'success': False,
                'why': Parameter.value_of('message_product_not_found_by_article', 'Не удалось найти товар с артикулом %s') % (ppk,)
            })
        try:
            size = get_object_or_404(AvailableSize, id=size_id)
        except Http404:
            return Response({
                'success': False,
                'why': Parameter.value_of('message_size_not_found_by_id', 'Не удалось найти нужный размер')
            })
        if not product.sizes.filter(id=size_id).exists():
            return Response({
                'success': False,
                'why': Parameter.value_of('message_product_has_no_size', 'Для товара %s недоступен размер %s') % (product, size)
            })
        return Response({
            'success': True,
            'product': str(product),
            'size': str(size),
            'quantity': info.add_to_scart(ppk, size.size, quantity)
        }) if info.add_to_scart(ppk, size.size, quantity, True) <= size.quantity else Response({
            'success': False,
            'why': Parameter.value_of('message_overkill', 'Извините, достигнут лимит. Это максимально возможное количество товаров в наличии.'),
            'available_quantity': size.quantity
        })
