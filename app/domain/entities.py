from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Product(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: str = Field(default="", max_length=2000, description="Product description")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    brand: str = Field(..., min_length=1, max_length=100, description="Product brand")
    stock_quantity: int = Field(default=0, ge=0, description="Stock quantity")
    is_active: bool = Field(default=True, description="Product active status")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}
    
    @field_validator('name', 'category', 'brand')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v
    
    def is_available(self) -> bool:
        """Check if product is available (active and has stock)"""
        return self.is_active and self.stock_quantity > 0
    
    def update_stock(self, quantity: int) -> None:
        """Update stock quantity with validation"""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self.stock_quantity = quantity
    
    def deactivate(self) -> None:
        """Deactivate the product"""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate the product"""
        self.is_active = True
    
    def is_valid(self) -> bool:
        """Validate product business rules"""
        try:
            # Check required fields are not empty
            if not self.name or not self.name.strip():
                return False
            if not self.category or not self.category.strip():
                return False  
            if not self.brand or not self.brand.strip():
                return False
            
            # Check price is positive
            if self.price <= 0:
                return False
            
            # Check stock is not negative
            if self.stock_quantity < 0:
                return False
                
            return True
        except Exception:
            return False