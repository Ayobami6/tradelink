from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
