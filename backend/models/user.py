from sqlalchemy import Boolean, Column, Integer, String, DateTime
from ..database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    role = Column(String, default="producer", nullable=False)  # producer, admin
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True, nullable=False)