from django.urls import path
from .views import (
    AddToCartView,
    RemoveFromCartView,
    CartDetail,
    CheckoutAPIView,
    PaystackWebhook,
)

urlpatterns = [
    path("carts/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("carts/remove/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("carts/", CartDetail.as_view(), name="cart-detail"),
    path("checkout/", CheckoutAPIView.as_view(), name="checkout"),
    path("paystack/webhook/", PaystackWebhook.as_view(), name="paystack-webhook"),
]
