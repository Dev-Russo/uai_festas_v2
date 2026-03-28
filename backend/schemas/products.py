from pydantic import BaseModel, Field, ConfigDict, NonNegativeFloat, field_validator
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    start_selling_date: Optional[datetime] = None
    end_selling_date: Optional[datetime] = None
    price: NonNegativeFloat = Field(default=0)
    available_quantity: Optional[int] = Field(
        default=None
    )
    is_active: bool = Field(default=True)

    @field_validator("start_selling_date", "end_selling_date", mode="before")
    @classmethod
    def empty_date_to_none(cls, value):
        # Frontends frequently send empty strings for blank datetime inputs.
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=50)
    start_selling_date: Optional[datetime] = None
    end_selling_date: Optional[datetime] = None
    price: Optional[NonNegativeFloat] =  None
    available_quantity: Optional[int] = Field(
        default=None
    )
    is_active: Optional[bool] = None

    @field_validator("start_selling_date", "end_selling_date", mode="before")
    @classmethod
    def empty_date_to_none(cls, value):
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
    
class ProductResponse(ProductBase):
    id: int
    event_id: int

    model_config = ConfigDict(from_attributes=True)

