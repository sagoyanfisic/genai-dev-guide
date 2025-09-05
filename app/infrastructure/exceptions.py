"""
Custom exceptions for AI services
"""

class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

class AIConfigurationError(AIServiceError):
    """Error in AI service configuration"""
    pass

class AIGenerationError(AIServiceError):
    """Error during AI content generation"""
    
    def __init__(self, message: str, service_name: str, original_error: Exception = None):
        self.service_name = service_name
        self.original_error = original_error
        super().__init__(f"{service_name}: {message}")

class AIValidationError(AIServiceError):
    """Error in input validation"""
    pass