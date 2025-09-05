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

@app.get("/debug-ai")
def debug_ai_service():
    """Debug endpoint para probar configuración de AI"""
    try:
        from app.core.config import settings
        from app.infrastructure.ai_factory import AIServiceFactory
        
        # Debug: mostrar configuración
        api_key = settings.get_google_api_key()
        use_vertex = getattr(settings, 'use_vertex_ai', False)
        
        debug_info = {
            "use_vertex_ai": use_vertex,
            "api_key_configured": bool(api_key),
            "api_key_length": len(api_key) if api_key else 0,
            "api_key_prefix": api_key[:10] + "..." if api_key and len(api_key) > 10 else api_key,
            "vertex_project_id": getattr(settings, 'vertex_ai_project_id', None),
            "vertex_location": getattr(settings, 'vertex_ai_location', None)
        }
        
        # Obtener información del servicio configurado
        service_info = AIServiceFactory.get_service_info()
        
        # Intentar crear servicio
        ai_service = AIServiceFactory.create_ai_service()
        
        # Probar generación de descripción simple
        test_description = ai_service.generate_product_description(
            name="Test Product",
            category="Electronics", 
            brand="TestBrand",
            basic_info="Simple test product"
        )
        
        return {
            "debug_info": debug_info,
            "service_info": service_info,
            "test_description": test_description,
            "status": "AI service working correctly"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "AI service configuration error",
            "debug_info": {
                "use_vertex_ai": getattr(settings, 'use_vertex_ai', None) if 'settings' in locals() else None,
                "api_key_configured": bool(settings.get_google_api_key()) if 'settings' in locals() and hasattr(settings, 'get_google_api_key') else False
            }
        }

@app.on_event("startup")
def startup_event():
    pass