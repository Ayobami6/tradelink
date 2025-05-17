from enum import Enum


class EnumBaseClass:

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class OrderStatus(EnumBaseClass, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentStatus(EnumBaseClass, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Courier(EnumBaseClass, Enum):
    DHL = "DHL"
    EXPRESS = "EXPRESS"


shipping_region = {
    "UK": "uk",
    "West Africa": "w_africa",
    "USA": "usa",
    "Europe": "europe",
    "East Africa": "e_africa",
    "Asia": "asia",
    "China": "china",
    "Caribbean": "caribbean",
}
