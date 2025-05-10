from django.shortcuts import render
from rest_framework import viewsets
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from rest_framework.views import APIView

from app.models import Product
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

    @exception_advice
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data)
        return service_response(
            data=data,
            message="Products retrieved successfully",
            status_code=200,
            status="success",
        )
