from django.db import models

# Create your models here.


class IPLog(models.Model):
    ip_address = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(
        max_length=100, null=True, blank=True, help_text="country of the ip address"
    )

    def __str__(self):
        return f"{self.ip_address} - {self.country}"
