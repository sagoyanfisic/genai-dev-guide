"""
Pytest configuration and shared fixtures
"""
import pytest
import asyncio
import os
from typing import Generator, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_database
from app.infrastructure.external_services import GeminiAIService


# Pytest asyncio configuration
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Database fixtures
@pytest.fixture
def mock_db_session():
    """Mock database session for unit tests"""
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
async def test_db_engine():
    """Create test database engine"""
    # Use in-memory SQLite for tests
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# API Client fixtures
@pytest.fixture
def test_client() -> TestClient:
    """Create test client for API testing"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client_with_db(mock_db_session) -> TestClient:
    """Create test client with mocked database"""
    app.dependency_overrides[get_database] = lambda: mock_db_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# AI Service fixtures
@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing"""
    service = MagicMock(spec=GeminiAIService)
    service.generate_product_description = AsyncMock(return_value="Mock description")
    service.generate_product_suggestions = AsyncMock(return_value="Mock suggestions")
    service.improve_product_description = AsyncMock(return_value="Improved description")
    service.get_service_info = MagicMock(return_value={"service": "mock", "model": "test"})
    return service


# Environment fixtures
@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables"""
    test_env_vars = {
        "ENVIRONMENT": "test",
        "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
        "GOOGLE_API_KEY": "test_api_key",
        "USE_VERTEX_AI": "false",
    }
    
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)


# Test data fixtures
@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Product",
        "category": "Test Category", 
        "brand": "Test Brand",
        "price": 99.99,
        "description": "Test description"
    }


@pytest.fixture
def sample_product_request():
    """Sample product creation request"""
    return {
        "name": "iPhone 15 Pro",
        "category": "Smartphones",
        "brand": "Apple",
        "price": 999.99,
        "basic_info": "Latest iPhone with A17 Pro chip"
    }