from django.shortcuts import render
from rest_framework import viewsets
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from rest_framework.views import APIView
from typing import List
from utils.utils import paginate
from django.db.models import Prefetch
from utils.constants import shipping_region

from app.models import Product, ProductAssets
from app.serializers import ProductSerializer

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


