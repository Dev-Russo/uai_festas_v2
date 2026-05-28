import uuid
from pydantic import BaseModel, Field, validator, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from enums.sales import SaleStatus, SaleKind

class SalesBase(BaseModel):
    buyer_name: str
    buyer_email: EmailStr
    buyer_cpf: str
    product_id: int
    method_of_payment: str
    sale_type: SaleKind = SaleKind.regular
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    status: SaleStatus

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    buyer_name: Optional[str] = None
    buyer_email: Optional[EmailStr] = None
    buyer_cpf: Optional[str] = None
    product_id: Optional[int] = None
    method_of_payment: Optional[str] = None
    sale_type: Optional[SaleKind] = None
    status: Optional[SaleStatus] = None

class SalesResponse(SalesBase):
    id: int
    price: float
    unique_code: uuid.UUID
    checkin_at: Optional[datetime] = None
    commissioner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class EmailRequest(BaseModel):
    to_email: Optional[EmailStr] = None
    subject: Optional[str] = None
    body: Optional[str] = None