from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()


class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    total_amount = serializers.FloatField()
    user_email = serializers.EmailField()
    payment_method = serializers.ChoiceField(choices=["card", "bank_transfer", "bank"])
