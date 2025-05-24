from django.shortcuts import render
from rest_framework.views import APIView

from orders.models import Order, OrderItem, PaystackTransaction
from .serializers import (
    AddToCartSerializer,
    CheckoutSerializer,
    RemoveFromCartSerializer,
)
from sparky_utils.advice import exception_advice
from sparky_utils.response import service_response
from utils.utils import generate_ref, PaystackSDK, get_client_ip

from app.models import Cart, ExchangeRate, Product, CartItem
from app.tasks import send_email_async
import hmac
import hashlib
from utils.constants import PaymentStatus
from utils.utils import get_client_ip, get_country_currency_from_ip
from utils.constants import country_currency_map, west_african_country_codes


# Create your views here.
class AddToCartView(APIView):

    @exception_advice()
    def post(self, request, *args, **kwargs):
        # get cart id from session
        cart_id = request.headers.get("cart")
        if not cart_id or cart_id == "":
            # create cart
            cart = Cart.objects.create()
            # save cart id to session
            # request.session["cart_id"] = str(cart.cart_id)
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
            "cart_id": cart.cart_id,
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
        cart_id = request.headers.get("cart")
        print("Let's see the cart: ", cart_id)
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
        cart_id = request.headers.get("cart")
        if not cart_id or cart_id == "":
            return service_response(
                data={},
                message="Cart not found",
                status_code=400,
                status="error",
            )
        cart = Cart.objects.get(cart_id=cart_id)
        is_local = False
        ip = get_client_ip(request)
        country = get_country_currency_from_ip(ip)
        if country in west_african_country_codes:
            is_local = True
        currency_details = country_currency_map.get(
            country, {"currency": "EUR", "symbol": "€"}
        )
        currency = currency_details.get("currency", "NGN")
        symbol = currency_details.get("symbol", "₦")
        exchange_rate = ExchangeRate.objects.get(currency_code=currency)
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
                    "total_price": float(cart_item.total_price()) * exchange_rate.rate,
                }
                for cart_item in cart.items.all()
            ],
            "total_price": float(cart.total_price()) * exchange_rate.rate,
            "all_items_weight": cart.total_items_weight(),
            "currency": currency,
            "symbol": symbol,
            "is_local": is_local,
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
        # get total item weight
        total_weight = cart.total_items_weight()
        if total_weight < 10.0:
            return service_response(
                data={},
                status="error",
                status_code=400,
                message="The minimum order weight is 10kg!",
            )
        total_payable_amount = float(cart.total_price()) + float(
            cart.calculated_shipping_fee
        )
        # create order
        order = Order.objects.create(
            total_amount=total_amount,
            user_email=user_email,
            payment_method=payment_method,
            order_ref=order_ref,
            shipping_address=cart.shipping_address,
            shipping_fee=float(cart.calculated_shipping_fee),
            total_payable_amount=float(total_payable_amount),
        )
        # add cart items to order
        for cart_item in cart.items.all():
            # create order item
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

        # initiatlize the paystack transaction
        data = {
            "reference": order_ref,
            "amount": int(total_payable_amount) * 100,
            "email": user_email,
            "channels": [payment_method],
        }
        paystack_sdk = PaystackSDK()
        status, response = paystack_sdk.initialize_transaction(
            data, int(total_payable_amount)
        )
        if not status:
            return service_response(
                data={},
                message="Payment initialization failed",
                status_code=400,
                status="error",
            )
        # send email
        subject: str = "Order Notification"
        message: str = (
            f"""Your order with reference {order_ref} has been received and is being processed and awaiting payment of {total_payable_amount}. Thank you for your patronage. \n
            with Items:
            {[{'product_name': cart_item.product.name, 'quantity': cart_item.quantity, "price": cart_item.total_price()} for cart_item in cart.items.all()]}
            """
        )
        # admin message
        admin_message: str = (
            f"An order with reference {order_ref} has been placed. Please login to the admin panel to process the order."
        )
        send_email_async.delay("customer", message, user_email, subject)
        send_email_async.delay("admin", admin_message, "ayobami@cross.africa", subject)
        # lets delete the cart
        cart.items.all().delete()
        return service_response(
            data=response,
            message="Payment initialized",
            status_code=200,
            status="success",
        )


class PaystackWebhook(APIView):
    PAYSTACK_IPS = {"52.31.139.75", "52.49.173.169", "52.214.14.220"}

    def post(self, request, *args, **kwargs):
        # check ip
        ip = get_client_ip(request)
        if ip not in self.PAYSTACK_IPS:
            return service_response(
                data={},
                message="Unauthorized",
                status_code=401,
                status="error",
            )
        # get the signature from the header
        signature = request.headers.get("X-Paystack-Signature")
        if not signature:
            return service_response(
                data={},
                message="Unauthorized",
                status_code=401,
                status="error",
            )
        # get the request body
        body = request.body
        # get the secret key from the environment
        secret_key = PaystackSDK().secret_key
        # verify the signature
        computed_signature = hmac.new(
            key=secret_key.encode("utf-8"), msg=body, digestmod=hashlib.sha512
        ).hexdigest()
        if not hmac.compare_digest(signature, computed_signature):
            return service_response(
                data={},
                message="Invalid signature",
                status_code=400,
                status="error",
            )
        # get the event from the request body
        event = request.data.get("event")
        if event == "charge.success":
            # get the reference from the request body
            reference = request.data.get("data").get("reference")
            # get the order from the database
            order = Order.objects.get(order_ref=reference)
            # update the order
            order.payment_status = PaymentStatus.COMPLETED.value
            order.save()
            # update paystack transaction object too
            paystack_transaction = PaystackTransaction.objects.get(order_ref=reference)
            paystack_transaction.status = PaymentStatus.COMPLETED.value
            paystack_transaction.confirmed = True
            paystack_transaction.save()

            # update the order items
            for order_item in order.items.all():
                order_item.product.reduce_available_quantity(order_item.quantity)
            # send email
            subject: str = "Order Payment Notification"
            message: str = (
                f"Your order with reference {reference} has been paid and is being processed. Thank you for your patronage."
            )
            send_email_async.delay("customer", message, order.user_email, subject)
            return service_response(
                data={},
                message="Payment successful",
                status_code=200,
                status="success",
            )
        return service_response(
            data={},
            message="Payment unsuccessful",
            status_code=400,
            status="error",
        )
