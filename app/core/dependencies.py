from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import ProductRepository
from app.infrastructure.external_services import GeminiAIService
from app.application.product_service import ProductService
from app.core.database import get_db

@lru_cache()
def get_ai_service() -> GeminiAIService:
    return GeminiAIService()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    product_repo = ProductRepository(db)
    ai_service = get_ai_service()
    
    return ProductService(product_repo, ai_service)