from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from app.models import Product

from utils.constants import OrderStatus, PaymentStatus
import uuid


# Create your models here.


class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    user_email = models.EmailField()
    total_amount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    order_status = models.CharField(
        max_length=200, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value
    )
    payment_status = models.CharField(
        max_length=200, default=PaymentStatus.PENDING.value, choices=PaymentStatus.choices()
    )
    shipping_address = models.TextField()
    shipping_fee = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    payment_method = models.CharField(
        max_length=200, choices=[("card", "Card"), ("bank", "Bank")], default="card"
    )
    order_ref = models.CharField(max_length=100, unique=True)
    total_payable_amount = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Total amount + shipping fee",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_payable_amount(self):
        total_amount = sum([item.subtotal() for item in self.items.all()])
        self.total_amount = total_amount
        self.total_payable_amount = total_amount + self.shipping_fee
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return float(self.product.price) * float(self.quantity)


class PaystackTransaction(models.Model):
    order_ref = models.CharField(max_length=200)
    amount = models.FloatField(default=0.0)
    confirmed = models.BooleanField(default=False)
    customer_email = models.EmailField()
    status = models.CharField(
        max_length=200, choices=PaymentStatus.choices(), default=PaymentStatus.PENDING.value
    )
    gateway_response = models.JSONField(null=True, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_ref} - {self.amount} - {self.status}"

    @classmethod
    def create_record(
        cls,
        order_ref,
        amount,
        customer_email,
        gateway_response,
        status=PaymentStatus.PENDING.value,
    ):
        return cls.objects.create(
            order_ref=order_ref,
            amount=amount,
            customer_email=customer_email,
            gateway_response=gateway_response,
            status=status,
        )
