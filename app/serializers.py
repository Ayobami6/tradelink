from rest_framework import serializers
from .models import Product, ProductAssets


class ProductAssetsSerializer(serializers.ModelSerializer):
    model = ProductAssets
    fields = ("name", "image", "alt")


class ProductSerializer(serializers.ModelSerializer):
    assets = ProductAssetsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "views",
            "discount_price",
            "top_deal",
            "created_at",
            "updated_at",
            "assets",
        )
