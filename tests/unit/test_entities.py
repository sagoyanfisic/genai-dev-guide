"""
Unit tests for domain entities
"""
import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.domain.entities import Product


class TestProduct:
    """Test Product entity"""
    
    def test_create_valid_product(self):
        """Test creating a valid product"""
        product = Product(
            name="iPhone 15",
            category="Smartphones", 
            brand="Apple",
            price=Decimal("999.99"),
            description="Latest iPhone"
        )
        
        assert product.name == "iPhone 15"
        assert product.category == "Smartphones"
        assert product.brand == "Apple"
        assert product.price == Decimal("999.99")
        assert product.description == "Latest iPhone"
    
    def test_product_name_validation(self):
        """Test product name validation"""
        # Empty name should fail
        with pytest.raises(ValidationError):
            Product(
                name="",
                category="Electronics",
                brand="Apple", 
                price=Decimal("100.00"),
                description="Test"
            )
        
        # Whitespace-only name should fail
        with pytest.raises(ValidationError):
            Product(
                name="   ",
                category="Electronics",
                brand="Apple",
                price=Decimal("100.00"),
                description="Test"
            )
    
    def test_product_price_validation(self):
        """Test product price validation"""
        # Zero price should fail
        with pytest.raises(ValidationError):
            Product(
                name="Test Product",
                category="Electronics",
                brand="Apple",
                price=Decimal("0.00"),
                description="Test"
            )
        
        # Negative price should fail
        with pytest.raises(ValidationError):
            Product(
                name="Test Product", 
                category="Electronics",
                brand="Apple",
                price=Decimal("-10.00"),
                description="Test"
            )
    
    def test_product_field_trimming(self):
        """Test that string fields are trimmed"""
        product = Product(
            name="  iPhone 15  ",
            category="  Smartphones  ",
            brand="  Apple  ",
            price=Decimal("999.99"),
            description="  Latest iPhone  "
        )
        
        assert product.name == "iPhone 15"
        assert product.category == "Smartphones" 
        assert product.brand == "Apple"
        assert product.description == "Latest iPhone"
    
    def test_product_serialization(self):
        """Test product serialization to dict"""
        product = Product(
            name="iPhone 15",
            category="Smartphones",
            brand="Apple", 
            price=Decimal("999.99"),
            description="Latest iPhone"
        )
        
        product_dict = product.model_dump()
        
        assert product_dict["name"] == "iPhone 15"
        assert product_dict["category"] == "Smartphones"
        assert product_dict["brand"] == "Apple"
        assert product_dict["price"] == Decimal("999.99")
        assert product_dict["description"] == "Latest iPhone"