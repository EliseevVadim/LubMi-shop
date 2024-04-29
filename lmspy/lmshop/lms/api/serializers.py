from rest_framework import serializers
from lms.models import Product, AvailableSize, Image


class AvailableSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSize
        fields = ['size', 'quantity']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['primary', 'image']


class ProductSerializer(serializers.ModelSerializer):
    sizes = AvailableSizeSerializer(many=True, read_only=True)
    primary_image = ImageSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['article', 'title', 'novelty', 'primary_image', 'sizes']


class ProductDetailSerializer(serializers.ModelSerializer):
    sizes = AvailableSizeSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['article', 'title', 'novelty', 'images', 'sizes']

