from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) 
    start_selling_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    end_selling_date = Column(DateTime(timezone=True), default=None)
    price = Column(Integer, nullable=False)

    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)

    #relationship with event
    event = relationship("Event", back_populates="products")
    #relationship with sales
    sales = relationship("Sales", back_populates="product")