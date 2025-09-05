"""
End-to-end tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestProductAPI:
    """Test Product API endpoints end-to-end"""
    
    def test_health_check(self, test_client: TestClient):
        """Test health check endpoint"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_create_product_endpoint(self, test_client_with_db: TestClient, sample_product_request):
        """Test creating a product via API"""
        response = test_client_with_db.post("/products/", json=sample_product_request)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_product_request["name"]
        assert data["category"] == sample_product_request["category"]
        assert data["brand"] == sample_product_request["brand"]
        assert "id" in data
        assert "created_at" in data
    
    def test_get_products_endpoint(self, test_client_with_db: TestClient):
        """Test getting products list via API"""
        response = test_client_with_db.get("/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_generate_description_endpoint(self, test_client_with_db: TestClient):
        """Test generating product description via API"""
        request_data = {
            "name": "iPhone 15",
            "category": "Smartphones", 
            "brand": "Apple",
            "basic_info": "Latest iPhone with A17 Pro"
        }
        
        response = test_client_with_db.post("/products/generate-description", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "description" in data
        assert isinstance(data["description"], str)
    
    def test_generate_suggestions_endpoint(self, test_client_with_db: TestClient):
        """Test generating product suggestions via API"""
        response = test_client_with_db.get("/products/suggestions/Laptops?count=3")
        
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert isinstance(data["suggestions"], str)
    
    def test_improve_description_endpoint(self, test_client_with_db: TestClient):
        """Test improving product description via API"""
        request_data = {
            "current_description": "Basic smartphone for daily use"
        }
        
        response = test_client_with_db.post("/products/improve-description", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "improved_description" in data
        assert isinstance(data["improved_description"], str)
    
    def test_invalid_product_creation(self, test_client_with_db: TestClient):
        """Test creating product with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should fail
            "category": "Electronics",
            "brand": "Apple",
            "price": -10.00  # Negative price should fail
        }
        
        response = test_client_with_db.post("/products/", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_nonexistent_endpoint(self, test_client: TestClient):
        """Test calling non-existent endpoint"""
        response = test_client.get("/nonexistent")
        
        assert response.status_code == 404


class TestAPIErrorHandling:
    """Test API error handling"""
    
    def test_malformed_json(self, test_client_with_db: TestClient):
        """Test sending malformed JSON"""
        response = test_client_with_db.post(
            "/products/",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, test_client_with_db: TestClient):
        """Test missing required fields in request"""
        incomplete_data = {
            "name": "Test Product"
            # Missing required fields: category, brand, price
        }
        
        response = test_client_with_db.post("/products/", json=incomplete_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data