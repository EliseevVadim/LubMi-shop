from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from lms.models import Product
from lms.api.serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLikeSetView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, pk, like: int, _=None):
        product = get_object_or_404(Product, pk=pk)
        like = bool(like)
        if product.favorite != like:
            pass  # TODO product.favorite = like
        return Response({
            'pk': pk,
            'like': like
        })


class ProductLikeToggleView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, pk, _=None):
        product = get_object_or_404(Product, pk=pk)
        like = True  # TODO -- remove this line --
        pass  # TODO -- product.favorite = (like := not product.favorite) --
        return Response({
            'pk': pk,
            'like': like
        })
