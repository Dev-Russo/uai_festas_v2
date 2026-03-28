from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    #verificar se os status são validos
    status: str = Field(default="Not Realized", max_length=20) #Não Realizado, Realizado, Cancelado.
    event_date: datetime = Field(default_factory=datetime.utcnow)
    sales_start_date: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = Field(default=None, min_length=5, max_length=200)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=20) #Não Realizado, Realizado, Cancelado.
    event_date: Optional[datetime] = None
    sales_start_date: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=200)
    
class EventResponse(EventBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)