from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ProductGroup(Base):
    __tablename__ = "product_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    parent_group_id = Column(Integer, ForeignKey("product_groups.id"), nullable=True)
    is_default = Column(Boolean, server_default="false", nullable=False)
    is_active = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event")
    parent = relationship("ProductGroup", back_populates="children", remote_side="ProductGroup.id")
    children = relationship("ProductGroup", back_populates="parent")
    memberships = relationship("ProductGroupMembership", back_populates="group", cascade="all, delete-orphan")


class ProductGroupMembership(Base):
    __tablename__ = "product_group_memberships"

    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("product_groups.id"), primary_key=True)
    is_active = Column(Boolean, server_default="true", nullable=False)

    product = relationship("Product")
    group = relationship("ProductGroup", back_populates="memberships")
