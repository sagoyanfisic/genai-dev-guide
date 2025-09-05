from typing import Type
from app.core.config import settings
from .ai_services import AIServiceInterface, GeminiDirectService, VertexAIService
import logging

logger = logging.getLogger(__name__)

class AIServiceFactory:
    """Factory para crear el servicio de AI apropiado basado en configuración"""
    
    @staticmethod
    def create_ai_service() -> AIServiceInterface:
        """
        Crea el servicio de AI basado en la configuración USE_VERTEX_AI
        
        Returns:
            AIServiceInterface: Instancia del servicio de AI configurado
        """
        if settings.use_vertex_ai:
            logger.info("🏭 Creating Vertex AI service")
            
            if not settings.vertex_ai_project_id:
                raise ValueError(
                    "VERTEX_AI_PROJECT_ID is required when USE_VERTEX_AI=true. "
                    "Set VERTEX_AI_PROJECT_ID or GCP_PROJECT_ID environment variable."
                )
            
            return VertexAIService(
                project_id=settings.vertex_ai_project_id,
                location=settings.vertex_ai_location
            )
        else:
            logger.info("🏭 Creating Gemini Direct service")
            
            if not settings.get_google_api_key():
                raise ValueError(
                    "GOOGLE_API_KEY is required when using Gemini Direct service. "
                    "Set GOOGLE_API_KEY environment variable."
                )
            
            return GeminiDirectService(api_key=settings.get_google_api_key())

    @staticmethod
    def get_service_info() -> dict:
        """
        Retorna información sobre el servicio de AI configurado
        
        Returns:
            dict: Información del servicio actual
        """
        if settings.use_vertex_ai:
            return {
                "service": "Vertex AI",
                "model": "gemini-2.0-flash",
                "project_id": settings.vertex_ai_project_id,
                "location": settings.vertex_ai_location,
                "use_vertex_ai": True
            }
        else:
            return {
                "service": "Gemini Direct",
                "model": "gemini-2.0-flash", 
                "api_key_configured": bool(settings.get_google_api_key()),
                "use_vertex_ai": False
            }