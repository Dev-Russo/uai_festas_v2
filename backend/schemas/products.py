from pydantic import BaseModel, EmailStr, Field, ConfigDict, NonNegativeFloat
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    start_selling_date: Optional[datetime] = None
    end_selling_date: Optional[datetime] = None
    price: NonNegativeFloat = Field(default=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=50)
    start_selling_date: Optional[datetime] = None
    end_selling_date: Optional[datetime] = None
    price: Optional[NonNegativeFloat] =  None

class ProductResponse(ProductBase):
    id: int
    event_id: int

    model_config = ConfigDict(from_attributes=True)

