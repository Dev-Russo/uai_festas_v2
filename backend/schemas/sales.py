from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class SalesBase(BaseModel):
    buyer_name: str
    price: int
    product_id: int
    method_of_payment: str
    sale_date: datetime = datetime.now()
    status: str

    @validator("status")
    def validate_status(cls, value):
        allowed_statuses = ["Payed", "Cancelled", "Check-in"]
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return value

class SalesCreate(SalesBase):
    pass

class SalesUpdate(SalesBase):
    buyer_name: Optional[str] = None
    price: Optional[int] = None
    product_id: Optional[int] = None
    method_of_payment: Optional[str] = None
    status: Optional[str] = None

class SalesResponse(SalesBase):
    id: int

    class Config:
        orm_mode = True