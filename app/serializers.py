from rest_framework import serializers
from .models import CartItem, Product, ProductAssets, Cart, ExchangeRate
from utils.utils import get_client_ip, get_country_currency_from_ip
from utils.constants import country_currency_map


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
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "assets",
            "weight_in_kg",
            "views",
            "discount_price",
            "available_quantity",
            "top_deal",
            "category",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        ip = get_client_ip(request)
        country = get_country_currency_from_ip(ip)
        data["country"] = country
        currency_details = country_currency_map.get(
            country, {"currency": "EUR", "symbol": "€"}
        )
        currency = currency_details.get("currency", "NGN")
        symbol = currency_details.get("symbol", "₦")
        data["currency"] = currency
        # get the exchange rate from the db
        try:
            exchange_rate = ExchangeRate.objects.get(currency_code=currency)
            price = data["price"] * exchange_rate.rate
            data["price"] = price
        except ExchangeRate.DoesNotExist:
            pass

        data["symbol"] = symbol
        return data


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
