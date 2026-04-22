from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Commissioner(Base):
    __tablename__ = "commissioners"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    commissioner_group_id = Column(Integer, nullable=True)  # FK adicionado na Feature 4
    role = Column(String, nullable=False, server_default="commissioner")
    full_access = Column(Boolean, nullable=False, server_default="false")
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event")
