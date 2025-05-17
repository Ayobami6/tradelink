from django.contrib import admin
from .models import CourierRate, Product, ProductAssets, Cart
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class ProductAssetsAdmin(admin.StackedInline):
    model = ProductAssets
    extra = 1
    fields = ("name", "image", "alt")


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAssetsAdmin]
    list_display = (
        "name",
        "price",
        "created_at",
        "updated_at",
        "available_quantity",
        "vendor_price",
        "weight_in_kg",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("views", "price")
    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):
        # add 20 % of the vendor price
        if obj.vendor_price:
            obj.price = obj.vendor_price + (float(obj.vendor_price) * 0.2)
        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "created_at", "updated_at", "no_items", "total_price")
    list_filter = ("created_at", "updated_at")
    search_fields = ("cart_id",)
    ordering = ("-created_at",)

    def no_items(self, obj):
        return obj.items.count()

    no_items.short_description = "No. of Items in Cart"

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Total Price"


class CourierRateResource(resources.ModelResource):
    class Meta:
        model = CourierRate
        fields = (
            "courier",
            "kg",
            "w_africa",
            "usa",
            "uk",
            "europe",
            "e_africa",
            "asia",
            "china",
            "caribbean",
        )
        import_id_fields = ("courier", "kg")
        import_order = ("courier", "kg")


@admin.register(CourierRate)
class CourierRateAdmin(ImportExportModelAdmin):
    resource_class = CourierRateResource
    list_display = (
        "courier",
        "kg",
        "w_africa",
        "usa",
        "uk",
        "europe",
        "e_africa",
        "asia",
        "china",
        "caribbean",
    )
    list_filter = ("courier",)
    search_fields = ("courier", "kg")
    ordering = ("courier", "kg")


admin.site.register(Product, ProductAdmin)
