from enum import Enum


class EnumBaseClass:

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]


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
