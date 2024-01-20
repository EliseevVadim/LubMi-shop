from rest_framework import serializers
from lms.models import Product, AvailableSize


class AvailableSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSize
        fields = ['size', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    sizes = AvailableSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['article', 'title', 'favorite', 'sizes']


