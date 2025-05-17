from django.shortcuts import render
from rest_framework.views import APIView

from orders.models import Order
from .serializers import (
    AddToCartSerializer,
    CheckoutSerializer,
    RemoveFromCartSerializer,
)
from sparky_utils.advice import exception_advice
from sparky_utils.response import service_response
from utils.utils import generate_ref, PaystackSDK

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
            "cart_id": cart.cart_id,
            "items_count": cart.total_items(),
            "items": [
                {
                    "product_id": cart_item.product.id,
                    "product_name": cart_item.product.name,
                    "product_price": cart_item.product.price,
                    "product_image": cart_item.product.assets.all()[0].image.url,
                    "quantity": cart_item.quantity,
                    "total_weight": cart_item.total_weight(),
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


# checkout view
class CheckoutAPIView(APIView):

    @exception_advice()
    def post(self, request, *args, **kwargs):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart_id = data.get("cart_id")
        total_amount = data.get("total_amount")
        user_email = data.get("user_email")
        payment_method = data.get("payment_method")
        order_ref = generate_ref()
        # get cart
        cart = Cart.objects.get(cart_id=cart_id)
        if not cart.shipping_address:
            return service_response(
                data={},
                message="Shipping address not provided",
                status_code=400,
                status="error",
            )
        total_payable_amount = float(cart.total_price()) + float(
            cart.calculated_shipping_fee
        )
        # create order
        _ = Order.objects.create(
            total_amount=total_amount,
            user_email=user_email,
            payment_method=payment_method,
            order_ref=order_ref,
            shipping_address=cart.shipping_address,
            shipping_fee=float(cart.calculated_shipping_fee),
            total_payable_amount=float(total_payable_amount),
        )
        # initiatlize the paystack transaction
        data = {
            "reference": order_ref,
            "amount": int(total_payable_amount) * 100,
            "email": user_email,
            "channels": [payment_method],
        }
        paystack_sdk = PaystackSDK()
        status, response = paystack_sdk.initialize_transaction(data)
        if not status:
            return service_response(
                data={},
                message="Payment initialization failed",
                status_code=400,
                status="error",
            )
        # send email
        return service_response(
            data=response,
            message="Payment initialized",
            status_code=200,
            status="success",
        )
