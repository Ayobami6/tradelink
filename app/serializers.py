from rest_framework import serializers
from .models import Product, ProductAssets


class ProductAssetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAssets
        fields = ("name", "image", "alt")


class ProductSerializer(serializers.ModelSerializer):
    assets = ProductAssetsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
