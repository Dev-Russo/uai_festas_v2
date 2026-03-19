from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=55) 
    email: EmailStr
    role: str = "producer" 
    is_active: bool = True

class UserCreate(UserBase):
    hashed_password: str = Field(min_length=8) 

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=55)
    email: Optional[EmailStr] = Field(default=None)
    role: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

class UserLogin(BaseModel):
    email: EmailStr
    passworld: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)