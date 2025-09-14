from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.models import Product
from app.routers.product_router import router as product_router

app = FastAPI(
    title="Product Catalog API",
    description="API para gestionar catálogo de productos con descripciones generadas por Gemini AI",
    version="1.0.0"
)

from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Product Catalog API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ai-status")
def ai_service_status():
    """Check Gemini AI service status"""
    try:
        from app.core.config import settings
        from app.infrastructure.external_services import GeminiAIService
        
        api_key = settings.get_google_api_key()
        
        if not api_key:
            return {
                "status": "error",
                "message": "GOOGLE_API_KEY not configured",
                "service": "Gemini Direct API"
            }
        
        # Test service initialization
        ai_service = GeminiAIService()
        service_info = ai_service.get_service_info()
        
        return {
            "status": "healthy",
            "message": "Gemini AI service is working correctly",
            **service_info
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"AI service error: {str(e)}",
            "service": "Gemini Direct API"
        }

@app.on_event("startup")
def startup_event():
    pass