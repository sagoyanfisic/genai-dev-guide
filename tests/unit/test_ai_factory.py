"""
Unit tests for AI Service Factory
"""
import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.ai_factory import AIServiceFactory
from app.infrastructure.ai_services import GeminiDirectService, VertexAIService
from app.infrastructure.exceptions import AIConfigurationError


class TestAIServiceFactory:
    """Test AI Service Factory"""
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_create_gemini_direct_service(self, mock_settings):
        """Test creating Gemini Direct service"""
        # Setup
        mock_settings.use_vertex_ai = False
        mock_settings.google_api_key = "test_api_key"
        
        with patch('app.infrastructure.ai_factory.GeminiDirectService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            # Act
            service = AIServiceFactory.create_ai_service()
            
            # Assert
            mock_service.assert_called_once_with(api_key="test_api_key")
            assert service == mock_instance
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_create_vertex_ai_service(self, mock_settings):
        """Test creating Vertex AI service"""
        # Setup
        mock_settings.use_vertex_ai = True
        mock_settings.vertex_ai_project_id = "test-project"
        mock_settings.vertex_ai_location = "us-central1"
        
        with patch('app.infrastructure.ai_factory.VertexAIService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            # Act
            service = AIServiceFactory.create_ai_service()
            
            # Assert
            mock_service.assert_called_once_with(
                project_id="test-project",
                location="us-central1"
            )
            assert service == mock_instance
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_create_gemini_service_missing_api_key(self, mock_settings):
        """Test creating Gemini service without API key raises error"""
        # Setup
        mock_settings.use_vertex_ai = False
        mock_settings.google_api_key = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AIServiceFactory.create_ai_service()
        
        assert "GOOGLE_API_KEY is required" in str(exc_info.value)
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_create_vertex_service_missing_project_id(self, mock_settings):
        """Test creating Vertex AI service without project ID raises error"""
        # Setup
        mock_settings.use_vertex_ai = True
        mock_settings.vertex_ai_project_id = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AIServiceFactory.create_ai_service()
        
        assert "VERTEX_AI_PROJECT_ID is required" in str(exc_info.value)
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_get_service_info_gemini(self, mock_settings):
        """Test getting service info for Gemini Direct"""
        # Setup
        mock_settings.use_vertex_ai = False
        mock_settings.google_api_key = "test_key"
        
        # Act
        info = AIServiceFactory.get_service_info()
        
        # Assert
        assert info["service"] == "Gemini Direct"
        assert info["model"] == "gemini-pro"
        assert info["use_vertex_ai"] is False
        assert info["api_key_configured"] is True
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_get_service_info_vertex_ai(self, mock_settings):
        """Test getting service info for Vertex AI"""
        # Setup
        mock_settings.use_vertex_ai = True
        mock_settings.vertex_ai_project_id = "test-project"
        mock_settings.vertex_ai_location = "us-west1"
        
        # Act
        info = AIServiceFactory.get_service_info()
        
        # Assert
        assert info["service"] == "Vertex AI"
        assert info["model"] == "gemini-pro"
        assert info["project_id"] == "test-project"
        assert info["location"] == "us-west1"
        assert info["use_vertex_ai"] is True
    
    @patch('app.infrastructure.ai_factory.settings')
    def test_get_service_info_gemini_no_api_key(self, mock_settings):
        """Test getting service info for Gemini without API key"""
        # Setup
        mock_settings.use_vertex_ai = False
        mock_settings.google_api_key = None
        
        # Act
        info = AIServiceFactory.get_service_info()
        
        # Assert
        assert info["service"] == "Gemini Direct"
        assert info["api_key_configured"] is False