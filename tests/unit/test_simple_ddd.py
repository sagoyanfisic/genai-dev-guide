import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from pydantic import ValidationError
from app.domain.entities import Product
from app.infrastructure.database import ProductRepository
from app.application.product_service import ProductService

@pytest.mark.unit
class TestProductEntity:
    def test_product_creation(self):
        product = Product(
            name="Test Product",
            price=Decimal("99.99"),
            category="Electronics",
            brand="TestBrand",
            stock_quantity=10
        )
        
        assert product.name == "Test Product"
        assert product.price == Decimal("99.99")
        assert product.is_available()

    def test_product_validation_success(self):
        # Test successful validation
        product = Product(
            name="Test Product",
            price=Decimal("10.50"),
            category="Electronics",
            brand="TestBrand"
        )
        assert product.name == "Test Product"
        assert product.price == Decimal("10.50")

    def test_product_validation_errors(self):
        # Test empty name
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="",
                price=Decimal("10.00"),
                category="Electronics",
                brand="TestBrand"
            )
        assert "Field cannot be empty" in str(exc_info.value)
        
        # Test invalid price
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=Decimal("0"),
                category="Electronics",
                brand="TestBrand"
            )
        assert "Price must be greater than 0" in str(exc_info.value)
        
        # Test negative stock
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=Decimal("10.00"),
                category="Electronics",
                brand="TestBrand",
                stock_quantity=-1
            )

    def test_stock_update(self):
        product = Product(
            name="Test",
            price=Decimal("10.00"),
            category="Electronics",
            brand="TestBrand"
        )
        product.update_stock(5)
        
        assert product.stock_quantity == 5
        
        with pytest.raises(ValueError):
            product.update_stock(-1)

    def test_product_activation(self):
        product = Product(
            name="Test",
            price=Decimal("10.00"),
            category="Electronics",
            brand="TestBrand"
        )
        product.deactivate()
        
        assert not product.is_active
        assert not product.is_available()  # Inactive products are not available
        
        product.activate()
        assert product.is_active

@pytest.mark.unit
class TestProductService:
    async def test_create_product_success(self):
        mock_product_repo = AsyncMock()
        mock_ai_service = AsyncMock()
        
        mock_product_repo.find_by_name.return_value = None
        mock_ai_service.generate_product_description.return_value = "AI generated description"
        
        created_product = Product(
            id=1, 
            name="Test Product",
            price=Decimal("99.99"),
            category="Electronics",
            brand="TestBrand",
            description="AI generated description"
        )
        mock_product_repo.save.return_value = created_product
        
        service = ProductService(mock_product_repo, mock_ai_service)
        
        result = await service.create_product(
            name="Test Product",
            price=Decimal("99.99"),
            category="Electronics",
            brand="TestBrand"
        )
        
        assert result.id == 1
        assert result.name == "Test Product"
        mock_ai_service.generate_product_description.assert_called_once()
        mock_product_repo.save.assert_called_once()

    async def test_create_product_already_exists(self):
        mock_product_repo = AsyncMock()
        mock_ai_service = AsyncMock()
        
        existing_product = Product(
            id=1, 
            name="Existing Product",
            price=Decimal("99.99"),
            category="Electronics",
            brand="TestBrand"
        )
        mock_product_repo.find_by_name.return_value = existing_product
        
        service = ProductService(mock_product_repo, mock_ai_service)
        
        with pytest.raises(Exception) as exc_info:
            await service.create_product(
                name="Existing Product",
                price=Decimal("99.99"),
                category="Electronics",
                brand="TestBrand"
            )
        
        assert "already exists" in str(exc_info.value)

    async def test_update_stock_success(self):
        mock_product_repo = AsyncMock()
        mock_ai_service = AsyncMock()
        
        product = Product(
            id=1, 
            name="Test",
            price=Decimal("10.00"),
            category="Electronics",
            brand="TestBrand",
            stock_quantity=5
        )
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.save.return_value = product
        
        service = ProductService(mock_product_repo, mock_ai_service)
        
        result = await service.update_stock(1, 10)
        
        assert result.stock_quantity == 10
        mock_product_repo.save.assert_called_once()

@pytest.mark.unit
class TestProductRepository:
    async def test_save_new_product(self):
        mock_session = AsyncMock()
        mock_db_product = MagicMock()
        mock_db_product.id = 1
        mock_db_product.created_at = "2024-01-01"
        mock_db_product.updated_at = "2024-01-01"
        
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        repo = ProductRepository(mock_session)
        
        with pytest.mock.patch('app.infrastructure.database.ProductModel') as mock_model:
            mock_model.return_value = mock_db_product
            
            product = Product(
                name="Test",
                price=Decimal("10.00"),
                category="Electronics",
                brand="TestBrand"
            )
            result = await repo.save(product)
            
            assert result.id == 1
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    async def test_find_by_id_not_found(self):
        mock_session = AsyncMock()
        mock_session.get.return_value = None
        
        repo = ProductRepository(mock_session)
        result = await repo.find_by_id(999)
        
        assert result is None