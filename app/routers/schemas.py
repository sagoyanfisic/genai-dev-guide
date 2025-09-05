from pydantic import BaseModel, Field, computed_field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category: str = Field(..., min_length=1, max_length=100)
    brand: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)
    basic_info: Optional[str] = Field(None, max_length=500)
    auto_generate_description: bool = True

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=2000)

class StockUpdateRequest(BaseModel):
    new_stock: int = Field(..., ge=0)

class ProductResponse(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    price: Decimal
    category: str
    brand: str
    stock_quantity: int
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    @computed_field
    @property
    def is_available(self) -> bool:
        return self.is_active and self.stock_quantity > 0
    
    class Config:
        from_attributes = True

class StockUpdateResponse(BaseModel):
    message: str
    new_stock: int

class MessageResponse(BaseModel):
    message: str

class CategorySuggestionsResponse(BaseModel):
    category: str
    suggestions: str