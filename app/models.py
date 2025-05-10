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

    top_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


@str_meta
class ProductAssets(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="assets"
    )
    image = CloudinaryField("image")
    alt = models.CharField(max_length=100, null=True, blank=True)


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
