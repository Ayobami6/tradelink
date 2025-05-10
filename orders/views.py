from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AddToCartSerializer, RemoveFromCartSerializer
from sparky_utils.advice import exception_advice
from sparky_utils.response import service_response

from app.models import Cart, Product, CartItem


# Create your views here.
class AddToCartView(APIView):

    @exception_advice()
    def post(self, request, *args, **kwargs):
        # get cart id from session
        cart_id = request.session.get("cart_id")
        if not cart_id:
            # create cart
            cart = Cart.objects.create()
            # save cart id to session
            request.session["cart_id"] = str(cart.cart_id)
        else:
            cart = Cart.objects.get(cart_id=cart_id)

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        # get the product
        product = Product.objects.get(id=product_id)
        # check if quantity is available
        if not product.is_available(quantity):
            return service_response(
                data={},
                message="Product not available",
                status_code=400,
                status="error",
            )

        # create cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        product.reduce_available_quantity(quantity)
        data = {
            "items_count": cart.total_items(),
        }
        return service_response(
            data=data,
            message="Product added to cart",
            status_code=201,
            status="success",
        )


class RemoveFromCartView(APIView):

    @exception_advice()
    def post(self, request, *args, **kwargs):
        # get cart id from session
        cart_id = request.session.get("cart_id")
        if not cart_id:
            return service_response(
                data={},
                message="Cart not found",
                status_code=400,
                status="error",
            )
        cart = Cart.objects.get(cart_id=cart_id)
        serializer = RemoveFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product_id = data.get("product_id")
        # get the product
        product = Product.objects.get(id=product_id)
        # get cart item
        cart_item = CartItem.objects.get(cart=cart, product=product)
        product.restock_available_quantity(cart_item.quantity)
        # delete cart item
        cart_item.delete()
        data = {
            "items_count": cart.total_items(),
        }
        return service_response(
            data=data,
            message="Product removed from cart",
            status_code=200,
            status="success",
        )


class CartDetail(APIView):

    @exception_advice()
    def get(self, request, *args, **kwargs):
        # get cart id from session
        cart_id = request.session.get("cart_id")
        if not cart_id:
            return service_response(
                data={},
                message="Cart not found",
                status_code=400,
                status="error",
            )
        cart = Cart.objects.get(cart_id=cart_id)
        data = {
            "items_count": cart.total_items(),
            "items": [
                {
                    "product_id": cart_item.product.id,
                    "product_name": cart_item.product.name,
                    "product_price": cart_item.product.price,
                    "product_image": cart_item.product.assets.all()[0].image.url,
                    "quantity": cart_item.quantity,
                    "total_price": cart_item.total_price(),
                }
                for cart_item in cart.items.all()
            ],
            "total_price": cart.total_price(),
        }
        return service_response(
            data=data,
            message="Cart details",
            status_code=200,
            status="success",
        )
