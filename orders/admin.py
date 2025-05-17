from django.contrib import admin
from .models import PaystackTransaction

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


admin.site.register(PaystackTransaction, PaystackTransactionAdmin)
