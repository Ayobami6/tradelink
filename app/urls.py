from django.urls import path, include
from .views import ProductViewSet, ShippingFeeAPIView, ShippingRegionAPIView
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
    path("shipping-regions/", ShippingRegionAPIView.as_view(), name="shipping-regions"),
    path("shipping-fee/", ShippingFeeAPIView.as_view(), name="shipping-fee"),
]
