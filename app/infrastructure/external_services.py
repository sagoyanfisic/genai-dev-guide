from .ai_factory import AIServiceFactory
from .ai_services import AIServiceInterface

class GeminiAIService:
    """
    Servicio de AI que usa el factory pattern para seleccionar entre Gemini Direct o Vertex AI
    """
    
    def __init__(self):
        self._ai_service: AIServiceInterface = AIServiceFactory.create_ai_service()
        self._service_info = AIServiceFactory.get_service_info()

    def generate_product_description(
        self, 
        name: str, 
        category: str, 
        brand: str, 
        basic_info: str = None
    ) -> str:
        """Genera una descripción detallada del producto usando el servicio de AI configurado"""
        return self._ai_service.generate_product_description(
            name=name,
            category=category, 
            brand=brand,
            basic_info=basic_info
        )

    def generate_product_suggestions(self, category: str, count: int = 5) -> str:
        """Genera sugerencias de productos para una categoría usando el servicio de AI configurado"""
        return self._ai_service.generate_product_suggestions(category, count)

    def improve_product_description(self, current_description: str) -> str:
        """Mejora una descripción existente del producto usando el servicio de AI configurado"""
        return self._ai_service.improve_product_description(current_description)
    
    def get_service_info(self) -> dict:
        """Retorna información sobre el servicio de AI actualmente configurado"""
        return self._service_info