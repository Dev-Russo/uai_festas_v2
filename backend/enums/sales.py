from enum import Enum

class SaleStatus(str, Enum):
    paid = "paid"
    cancelled = "cancelled"
    refunded = "refunded"
    pending = "pending"