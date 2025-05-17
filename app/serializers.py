from rest_framework import serializers
from .models import CartItem, Product, ProductAssets, Cart


class ProductAssetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAssets
        fields = ("name", "image", "alt")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image_url = instance.image.url
        data["image"] = image_url
        return data


class ProductSerializer(serializers.ModelSerializer):
    assets = ProductAssetsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "items"]


class ShippingFeeSerializer(serializers.Serializer):
    cart_id = serializers.CharField()
    shipping_region = serializers.CharField()
    courier = serializers.CharField()
    email = serializers.EmailField()
    shipping_address = serializers.CharField()
