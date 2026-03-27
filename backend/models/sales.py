from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from backend.database import Base

class Sales(Base):
    __tableneme__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    method_of_payment = Column(String, nullable=False)

    #relationship with product
    product = relationship("Product", back_populates="sales")