from app.core.config import settings
from .ai_services import AIServiceInterface, GeminiDirectService
import logging

logger = logging.getLogger(__name__)

class AIServiceFactory:
    """Factory para crear el servicio de Gemini Direct API únicamente"""
    
    @staticmethod
    def create_ai_service() -> AIServiceInterface:
        """
        Crea el servicio de Gemini Direct API
        
        Returns:
            AIServiceInterface: Instancia del servicio de Gemini Direct
        """
        logger.info("🏭 Creating Gemini Direct service (only supported service)")
        
        if not settings.get_google_api_key():
            raise ValueError(
                "GOOGLE_API_KEY is required for Gemini Direct service. "
                "Set GOOGLE_API_KEY environment variable."
            )
        
        return GeminiDirectService(api_key=settings.get_google_api_key())

    @staticmethod
    def get_service_info() -> dict:
        """
        Retorna información sobre el servicio de Gemini Direct
        
        Returns:
            dict: Información del servicio Gemini Direct
        """
        return {
            "service": "Gemini Direct API",
            "model": "gemini-2.0-flash", 
            "api_key_configured": bool(settings.get_google_api_key()),
            "use_vertex_ai": False,
            "note": "Only Gemini Direct API is supported in this configuration"
        }