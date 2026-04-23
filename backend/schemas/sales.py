import uuid
from pydantic import BaseModel, Field, validator, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from enums.sales import SaleStatus

class SalesBase(BaseModel):
    buyer_name: str
    buyer_email: EmailStr
    product_id: int
    method_of_payment: str
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    status: SaleStatus

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    buyer_name: Optional[str] = None
    buyer_email: Optional[EmailStr] = None
    product_id: Optional[int] = None
    method_of_payment: Optional[str] = None
    status: Optional[SaleStatus] = None

class SalesResponse(SalesBase):
    id: int
    price: float
    unique_code: uuid.UUID
    checkin_at: Optional[datetime] = None

    
    model_config = ConfigDict(from_attributes=True)