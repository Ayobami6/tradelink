from django.db import models
from sparky_utils.decorators import str_meta
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.


@str_meta
class Product(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)

    available_quantity = models.IntegerField(default=0)

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

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def total_items(self):
        return len(self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
