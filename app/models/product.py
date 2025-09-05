from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, DECIMAL
from sqlalchemy.sql import func
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())