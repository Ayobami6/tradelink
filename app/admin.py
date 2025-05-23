from django.contrib import admin
from .models import (
    CourierRate,
    Product,
    ProductAssets,
    Cart,
    AppSetting,
    ExchangeRate,
    ProductCategory,
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class AppSettingAdmin(admin.ModelAdmin):
    list_display = ("name", "whatapp_business_url")


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
        "global_price",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("views", "price")
    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):
        # add 20 % of the vendor price
        if obj.vendor_price:
            percentage_multiplier = 0.2
            # update global by 20 %
            obj.global_price = obj.vendor_price + (
                float(obj.vendor_price) * percentage_multiplier
            )
            if obj.use_custom_fee_percentage:
                percentage_multiplier = float(obj.custom_fee_percentage)
            obj.price = obj.vendor_price + (
                float(obj.vendor_price) * percentage_multiplier
            )
        super().save_model(request, obj, form, change)

    def update_global_price(self, request, queryset):
        for product in queryset:
            product.global_price = float(product.vendor_price) + (
                float(product.vendor_price) * 0.2
            )
            product.save()
        self.message_user(
            request, f"{queryset.count()} product(s) global price updated successfully."
        )

    update_global_price.short_description = "Update Global Price"
    actions = ["update_global_price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "cart_id",
        "created_at",
        "updated_at",
        "no_items",
        "total_price",
        "weight",
        "customer_email",
        "calculated_shipping_fee",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("cart_id",)
    ordering = ("-created_at",)

    def no_items(self, obj):
        return obj.items.count()

    no_items.short_description = "No. of Items in Cart"

    def total_price(self, obj):
        return obj.total_price()

    def weight(self, obj):
        return obj.total_items_weight()

    weight.short_description = "Total Weight in KG"

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
    actions = ["remove_w_africa_fee"]

    # add remove shipping fee for w_africa
    def remove_w_africa_fee(self, request, queryset):
        updated = queryset.update(w_africa=0.0)
        self.message_user(request, f"{updated} item(s) marked as flagged.")

    remove_w_africa_fee.short_description = "Remove W Africa Fee"


class ExcahngeRateAdmin(admin.ModelAdmin):
    list_display = ("currency_code", "rate")
    list_filter = ("currency_code",)
    search_fields = ("currency_code",)
    ordering = ("currency_code",)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ExchangeRate, ExcahngeRateAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(AppSetting, AppSettingAdmin)
