from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=55) 
    email: EmailStr
    role: str = "producer" 
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=8) 

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=55)
    email: Optional[EmailStr] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None