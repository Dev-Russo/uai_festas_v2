from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
from backend.enums.sales import SaleStatus

class SalesBase(BaseModel):
    buyer_name: str
    buyer_email: EmailStr
    price: int
    product_id: int
    method_of_payment: str
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    status: SaleStatus

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    buyer_name: Optional[str] = None
    buyer_email: Optional[EmailStr] = None
    price: Optional[int] = None
    product_id: Optional[int] = None
    method_of_payment: Optional[str] = None
    status: Optional[SaleStatus] = None

class SalesResponse(SalesBase):
    id: int

    class Config:
        orm_mode = True