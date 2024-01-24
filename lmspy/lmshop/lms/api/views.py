from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from lms.models import Product
from lms.api.serializers import ProductSerializer
from customerinfo.customerinfo import CustomerInfo
from json import JSONDecodeError
import json


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


class GetCustomerInfo(APIView):
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


class NotifyMeForDelivery(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, _=None):
        try:
            cui = json.loads(request.body)
            print(cui)
            info = CustomerInfo(request)
            return Response({'ok': True})
        except JSONDecodeError:
            return Response({'ok': False})
        except KeyError:
            return Response({'ok': False})

