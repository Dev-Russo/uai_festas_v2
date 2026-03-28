from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from database import Base

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    status = Column(String, index=True, default="Not Realized", nullable=False) #Não Realizado, Realizado, Cancelado.
    event_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    sales_start_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #relationship with user
    owner = relationship("User", back_populates="events")
    products = relationship("Product", back_populates="event")
    