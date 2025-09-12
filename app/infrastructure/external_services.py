from app.core.config import settings
from .ai_services import GeminiDirectService
from .exceptions import AIConfigurationError
import logging

logger = logging.getLogger(__name__)

class GeminiAIService:
    """
    Servicio optimizado de Gemini AI - solo soporta Gemini Direct API
    """
    
    def __init__(self):
        """Initialize Gemini Direct service"""
        api_key = settings.get_google_api_key()
        if not api_key:
            raise AIConfigurationError("GOOGLE_API_KEY is required for Gemini service")
        
        self._ai_service = GeminiDirectService(api_key=api_key)
        logger.info("🚀 Gemini AI Service initialized successfully")

    def generate_product_description(
        self, 
        name: str, 
        category: str, 
        brand: str, 
        basic_info: str = None
    ) -> str:
        """Genera una descripción detallada del producto usando Gemini"""
        return self._ai_service.generate_product_description(
            name=name,
            category=category, 
            brand=brand,
            basic_info=basic_info
        )

    def generate_product_suggestions(self, category: str, count: int = 5) -> str:
        """Genera sugerencias de productos para una categoría usando Gemini"""
        return self._ai_service.generate_product_suggestions(category, count)

    def improve_product_description(self, current_description: str) -> str:
        """Mejora una descripción existente del producto usando Gemini"""
        return self._ai_service.improve_product_description(current_description)
    
    def get_service_info(self) -> dict:
        """Retorna información sobre el servicio de Gemini"""
        return {
            "service": "Gemini Direct API",
            "model": "gemini-2.0-flash",
            "status": "active"
        }