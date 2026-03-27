from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String, index=True, nullable=False)
    buyer_email = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    method_of_payment = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False) #paid, cancelled, check_in
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    #relationship with product
    product = relationship("Product", back_populates="sales")