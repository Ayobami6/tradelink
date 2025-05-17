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
        max_length=20, choices=OrderStatus.choices(), default=OrderStatus.PENDING
    )
    payment_status = models.CharField(
        max_length=20, default=PaymentStatus.PENDING, choices=PaymentStatus.choices()
    )
    shipping_address = models.TextField()
    shipping_fee = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    order_ref = models.CharField(max_length=20, unique=True)
    total_payable_amount = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Total amount + shipping fee",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

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
