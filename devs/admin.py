from django.contrib import admin

from devs.models import IPLog

# Register your models here.


class IPLogAdmin(admin.ModelAdmin):
    list_display = [
        "ip_address",
        "country",
    ]
    search_fields = ["ip_address", "country"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]


admin.site.register(IPLog, IPLogAdmin)
