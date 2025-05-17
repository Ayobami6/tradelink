from django.shortcuts import render
from rest_framework import viewsets
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from rest_framework.views import APIView
from typing import List
from utils.utils import paginate
from django.db.models import Prefetch
from utils.constants import Courier, shipping_region

from app.models import Cart, CourierRate, Product, ProductAssets
from app.serializers import ProductSerializer, ShippingFeeSerializer

# Create your views here.


# root view
class RootPage(APIView):
    def get(self, request):
        return service_response(
            data={"message": "Welcome to the tradelink API"},
            message="Welcome to the tradelink API",
            status_code=200,
            status="success",
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @exception_advice()
    def list(self, request, *args, **kwargs):
        assets_fields: List[str] = ["name", "image", "alt"]
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        products = Product.objects.prefetch_related(
            Prefetch("assets", queryset=ProductAssets.objects.only(*assets_fields))
        ).all()
        response = paginate(products, int(page), request, int(size), ProductSerializer)
        return service_response(
            data=response,
            message="Products retrieved successfully",
            status_code=200,
            status="success",
        )

    @exception_advice()
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return service_response(
            data=serializer.data,
            message="Product retrieved successfully",
            status_code=200,
            status="success",
        )


class ShippingRegionAPIView(APIView):
    """Returns the shipping regions"""

    def get(self, request, *args, **kwargs):
        return service_response(
            data=shipping_region,
            message="Shipping regions retrieved successfully",
            status_code=200,
            status="success",
        )


class ShippingFeeAPIView(APIView):
    """Returns the shipping fee"""

    def post(self, request, *args, **kwargs):
        serializer = ShippingFeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart_id = data.get("cart_id")
        shipping_region = data.get("shipping_region")
        courier = data.get("courier")
        courier_choices = Courier.values()
        if courier not in courier_choices:
            return service_response(
                data={},
                message="Unsupported logistics courier",
                status_code=400,
                status="error",
            )
        cart = Cart.objects.get(cart_id=cart_id)
        total_weight = cart.total_items_weight()
        courier_rate = CourierRate.objects.filter(
            courier=courier, kg__gte=total_weight
        ).first()
        # get the rate for the shipping region
        shipping_fee = courier_rate.__getattribute__(shipping_region)
        return service_response(
            data={"shipping_fee": shipping_fee},
            message="Shipping fee retrieved successfully",
            status_code=200,
            status="success",
        )
