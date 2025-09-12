from abc import ABC, abstractmethod
from typing import Optional
import asyncio
import logging
from .prompts import (
    format_product_description_prompt,
    format_product_suggestions_prompt,
    format_improve_description_prompt
)
from .exceptions import AIGenerationError, AIConfigurationError, AIValidationError

logger = logging.getLogger(__name__)

class AIServiceInterface(ABC):
    """Interface común para servicios de AI"""
    
    @abstractmethod
    def generate_product_description(
        self, 
        name: str, 
        category: str, 
        brand: str, 
        basic_info: Optional[str] = None
    ) -> str:
        """Generate product description"""
        pass

    @abstractmethod 
    def generate_product_suggestions(self, category: str, count: int = 5) -> str:
        """Generate product suggestions for a category"""
        pass

    @abstractmethod
    def improve_product_description(self, current_description: str) -> str:
        """Improve existing product description"""
        pass
    
    def _validate_inputs(self, **kwargs) -> None:
        """Validate input parameters"""
        for key, value in kwargs.items():
            if isinstance(value, str) and not value.strip():
                raise AIValidationError(f"Parameter '{key}' cannot be empty")
            if key == 'count' and (not isinstance(value, int) or value <= 0):
                raise AIValidationError("Parameter 'count' must be a positive integer")

class BaseAIService(AIServiceInterface):
    """Base implementation with common functionality"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self._model = None
        self._generation_config = None
    
    def _generate_sync(self, prompt: str) -> str:
        """Generate content synchronously"""
        if not self._model:
            raise AIGenerationError("Model not initialized", self.service_name)
        
        try:
            response = self._model.generate_content(
                prompt,
                generation_config=self._generation_config
            )
            if not response or not response.text:
                raise AIGenerationError("Empty response from AI service", self.service_name)
            return response.text
        except Exception as e:
            raise AIGenerationError(f"Content generation failed: {str(e)}", self.service_name, e)

    def generate_product_description(
        self, 
        name: str, 
        category: str, 
        brand: str, 
        basic_info: Optional[str] = None
    ) -> str:
        """Generate product description using AI"""
        try:
            self._validate_inputs(name=name, category=category, brand=brand)
            
            logger.info(f"Generating product description with {self.service_name} for: {name}")
            prompt = format_product_description_prompt(name, category, brand, basic_info)
            response = self._generate_sync(prompt)
            
            logger.info(f"Successfully generated description with {self.service_name}")
            return response.strip()
            
        except AIValidationError:
            raise
        except Exception as e:
            logger.error(f"Error generating description with {self.service_name}: {str(e)}")
            raise AIGenerationError(f"Failed to generate description: {str(e)}", self.service_name, e)

    def generate_product_suggestions(self, category: str, count: int = 5) -> str:
        """Generate product suggestions for a category"""
        try:
            self._validate_inputs(category=category, count=count)
            
            logger.info(f"Generating {count} product suggestions with {self.service_name} for category: {category}")
            prompt = format_product_suggestions_prompt(category, count)
            response = self._generate_sync(prompt)
            
            logger.info(f"Successfully generated suggestions with {self.service_name}")
            return response.strip()
            
        except AIValidationError:
            raise
        except Exception as e:
            logger.error(f"Error generating suggestions with {self.service_name}: {str(e)}")
            raise AIGenerationError(f"Failed to generate suggestions: {str(e)}", self.service_name, e)

    def improve_product_description(self, current_description: str) -> str:
        """Improve existing product description"""
        try:
            self._validate_inputs(current_description=current_description)
            
            logger.info(f"Improving product description with {self.service_name}")
            prompt = format_improve_description_prompt(current_description)
            response = self._generate_sync(prompt)
            
            logger.info(f"Successfully improved description with {self.service_name}")
            return response.strip()
            
        except AIValidationError:
            raise
        except Exception as e:
            logger.error(f"Error improving description with {self.service_name}: {str(e)}")
            raise AIGenerationError(f"Failed to improve description: {str(e)}", self.service_name, e)

class GeminiDirectService(BaseAIService):
    """Servicio usando Gemini API directamente"""
    
    def __init__(self, api_key: str):
        super().__init__("Gemini Direct")
        
        if not api_key or not api_key.strip():
            raise AIConfigurationError("Google API key is required")
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel('gemini-2.0-flash')
            
            self._generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=1024,
            )
            
            logger.info(f"🚀 {self.service_name} initialized successfully")
            
        except ImportError as e:
            raise AIConfigurationError(f"Google Generative AI SDK not installed: {e}")
        except Exception as e:
            raise AIConfigurationError(f"Failed to initialize {self.service_name}: {e}")

# VertexAIService removed - Only Gemini Direct API is supported