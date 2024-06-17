from rest_framework import serializers
from lms.models import Product, AvailableSize, Image, AboutItem


class AvailableSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSize
        fields = ['id', 'size', 'quantity']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['primary', 'image']


class ProductSerializer(serializers.ModelSerializer):
    sizes = AvailableSizeSerializer(many=True, read_only=True)
    primary_image = ImageSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = [
            'article',
            'title',
            'color',
            'description',
            'novelty',
            'actual_price',
            'old_price',
            'in_stock',
            'primary_image',
            'sizes',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    sizes = AvailableSizeSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'article',
            'title',
            'description',
            'novelty',
            'actual_price',
            'old_price',
            'in_stock',
            'images',
            'sizes',
        ]


class AboutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutItem
        fields = [
            'image',
            'label',
            'description',
            'kind',
            'link',
        ]
