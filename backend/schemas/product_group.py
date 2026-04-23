from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductSummary(BaseModel):
    id: int
    name: str
    price: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class MembershipResponse(BaseModel):
    product_id: int
    group_id: int
    is_active: bool
    product: ProductSummary

    model_config = ConfigDict(from_attributes=True)


class MembershipToggle(BaseModel):
    is_active: bool


class ProductGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_group_id: Optional[int] = None
    is_default: bool = False


class ProductGroupUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductGroupResponse(BaseModel):
    id: int
    name: str
    event_id: int
    parent_group_id: Optional[int] = None
    is_default: bool
    is_active: bool
    children: list[ProductGroupResponse] = []
    memberships: list[MembershipResponse] = []

    model_config = ConfigDict(from_attributes=True)


ProductGroupResponse.model_rebuild()
