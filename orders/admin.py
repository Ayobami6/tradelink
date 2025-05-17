from django.contrib import admin
from .models import PaystackTransaction, Order, OrderItem

# Register your models here.


class PaystackTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "order_ref",
        "amount",
        "customer_email",
        "status",
        "transaction_date",
        "updated_at",
    ]
    search_fields = ["order_ref", "customer_email"]
    list_filter = ["status", "transaction_date"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_ref",
        "user_email",
        "payment_status",
        "total_amount",
        "total_payable_amount",
        "payment_method",
        "shipping_fee",
        "order_status",
        "created_at",
    ]
    search_fields = ["order_ref", "user_email"]
    list_filter = ["payment_status", "created_at", "order_status", "payment_method"]
    ordering = ["-created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order__order_ref",
        "product__name",
        "quantity",
        "total_price",
    ]
    search_fields = ["order__order_ref", "product__name"]
    ordering = ["-order__created_at"]

    def total_price(self, obj):
        return float(obj.product.price) * float(obj.quantity)

    total_price.short_description = "Total Price"


admin.site.register(PaystackTransaction, PaystackTransactionAdmin)
admin.site.register(Order, OrderAdmin)
