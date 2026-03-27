from enum import Enum

class SaleStatus(str, Enum):
    paid = "paid"
    cancelled = "cancelled"
    check_in = "check_in"