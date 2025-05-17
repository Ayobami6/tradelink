from django.db import models
from sparky_utils.decorators import str_meta
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator

from utils.constants import Courier

# Create your models here.


@str_meta
class Product(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=500)
    price = models.FloatField(editable=False)
    description = models.TextField(null=True, blank=True)
    vendor_price = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    views = models.IntegerField(default=0)
    weight_in_kg = models.CharField(
        max_length=100, help_text="Product weight in kg", null=True
    )
    discount_price = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.0)]
    )

    available_quantity = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )

    top_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def is_available(self, quantity: int) -> bool:
        """checks if the quantity to purchase is available

        Args:
            quantity (int): quantity to check for

        Returns:
            bool: True/False
        """
        return self.available_quantity >= quantity

    def reduce_available_quantity(self, quantity: int):
        self.available_quantity -= quantity
        self.save()

    def restock_available_quantity(self, quantity: int):
        self.available_quantity += quantity
        self.save()


@str_meta
class ProductAssets(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="assets"
    )
    image = CloudinaryField("image")
    alt = models.CharField(max_length=100, null=True, blank=True)


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def total_items(self):
        return len(self.items.all())

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class CourierRate(models.Model):
    """Partner logistics Rate"""

    id = models.BigAutoField(primary_key=True)

    kg = models.FloatField(validators=[MinValueValidator(0.0)])
    uk = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="UK rate per kg"
    )
    w_africa = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="West Africa rate per kg"
    )
    usa = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="USA rate per kg"
    )
    europe = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="Europe rate per kg"
    )
    e_africa = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="East Africa rate per kg"
    )
    asia = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="Asia rate per kg"
    )
    china = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="China rate per kg"
    )
    caribbean = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="Caribbean rate per kg"
    )
    courier = models.CharField(
        max_length=100, null=True, blank=True, choices=Courier.choices()
    )

    def __str__(self) -> str:
        return f"{self.courier} {self.kg}kg"

    class Meta:
        verbose_name_plural = "Partners Logistics Courier Rates"
        verbose_name = "Partners Logistics Courier Rate"
