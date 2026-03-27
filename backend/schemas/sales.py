from pydantic import BaseModel
from typing import Optional


class SalesBase(BaseModel):
    buyer_name: str
    price: int
    product_id: int
    method_of_payment: str

class SalesCreate(SalesBase):
    pass

class SalesUpdate(SalesBase):
    buyer_name: Optional[str] = None
    price: Optional[int] = None
    product_id: Optional[int] = None
    method_of_payment: Optional[str] = None

class SalesResponse(SalesBase):
    id: int

    class Config:
        orm_mode = True