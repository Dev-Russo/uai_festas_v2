import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
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
    status = Column(String, index=True, nullable=False) #paid, cancelled, refunded, pending
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    checkin_at = Column(DateTime(timezone=True), nullable=True)
    unique_code = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    #relationship with product
    product = relationship("Product", back_populates="sales")