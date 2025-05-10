from django.urls import path
from .views import AddToCartView, RemoveFromCartView

urlpatterns = [
    path("carts/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("carts/remove/", RemoveFromCartView.as_view(), name="remove-from-cart"),
]
