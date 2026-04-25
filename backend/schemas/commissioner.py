from pydantic import BaseModel, ConfigDict, Field
from enums.commissioner import CommissionerRole
from typing import Optional

class CommissionerBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=1, max_length=55)
    role: CommissionerRole = CommissionerRole.commissioner
    full_access: bool = False
    is_active: bool = True

class CommissionerCreate(CommissionerBase):
    password: str = Field(min_length=8)

class CommissionerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=55)
    role: Optional[CommissionerRole] = None
    full_access: Optional[bool] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=8)
    commissioner_group_id: Optional[int] = None

class CommissionerResponse(CommissionerBase):
    id: int
    event_id: int
    commissioner_group_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
