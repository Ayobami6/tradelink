from django.contrib import admin
from .models import Product, ProductAssets

# Register your models here.


class ProductAssetsAdmin(admin.StackedInline):
    model = ProductAssets
    extra = 1
    fields = ("name", "image", "alt")


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAssetsAdmin]
    list_display = ("name", "price", "created_at", "updated_at", "available_quantity")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


admin.site.register(Product, ProductAdmin)
