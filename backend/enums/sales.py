from enum import Enum

class SaleStatus(str, Enum):
    paid = "paid"
    cancelled = "cancelled"
    refunded = "refunded"
    pending = "pending"

class SaleKind(str, Enum):
    regular = "regular"
    courtesy = "courtesy"