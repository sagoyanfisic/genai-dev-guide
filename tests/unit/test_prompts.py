"""
Unit tests for AI prompts
"""
import pytest
from app.infrastructure.prompts import (
    format_product_description_prompt,
    format_product_suggestions_prompt,
    format_improve_description_prompt,
    PRODUCT_DESCRIPTION_BASE_PROMPT,
    PRODUCT_SUGGESTIONS_PROMPT,
    IMPROVE_DESCRIPTION_PROMPT
)


class TestPromptFormatting:
    """Test prompt formatting functions"""
    
    def test_product_description_prompt_basic(self):
        """Test basic product description prompt formatting"""
        prompt = format_product_description_prompt(
            name="iPhone 15",
            category="Smartphones",
            brand="Apple"
        )
        
        assert "iPhone 15" in prompt
        assert "Smartphones" in prompt
        assert "Apple" in prompt
        assert "descripción atractiva" in prompt
    
    def test_product_description_prompt_with_basic_info(self):
        """Test product description prompt with additional info"""
        prompt = format_product_description_prompt(
            name="iPhone 15",
            category="Smartphones", 
            brand="Apple",
            basic_info="A17 Pro chip"
        )
        
        assert "iPhone 15" in prompt
        assert "A17 Pro chip" in prompt
        assert "Información adicional: A17 Pro chip" in prompt
    
    def test_product_description_prompt_without_basic_info(self):
        """Test product description prompt without additional info"""
        prompt = format_product_description_prompt(
            name="iPhone 15",
            category="Smartphones",
            brand="Apple",
            basic_info=None
        )
        
        assert "iPhone 15" in prompt
        assert "Información adicional:" not in prompt
    
    def test_product_suggestions_prompt(self):
        """Test product suggestions prompt formatting"""
        prompt = format_product_suggestions_prompt(
            category="Laptops",
            count=3
        )
        
        assert "Laptops" in prompt
        assert "3 productos" in prompt
        assert "lista de 3" in prompt.lower()
    
    def test_product_suggestions_prompt_default_count(self):
        """Test product suggestions prompt with default count"""
        prompt = format_product_suggestions_prompt(category="Smartphones")
        
        assert "Smartphones" in prompt
        assert "5 productos" in prompt
    
    def test_improve_description_prompt(self):
        """Test improve description prompt formatting"""
        current_description = "Basic phone description"
        prompt = format_improve_description_prompt(current_description)
        
        assert current_description in prompt
        assert "Mejora la siguiente descripción" in prompt
        assert "más atractiva y completa" in prompt


class TestPromptConstants:
    """Test that prompt constants are properly defined"""
    
    def test_prompt_constants_exist(self):
        """Test that all prompt constants are defined"""
        assert PRODUCT_DESCRIPTION_BASE_PROMPT is not None
        assert PRODUCT_SUGGESTIONS_PROMPT is not None
        assert IMPROVE_DESCRIPTION_PROMPT is not None
    
    def test_prompt_constants_have_placeholders(self):
        """Test that prompt constants have required placeholders"""
        # Product description prompt
        assert "{name}" in PRODUCT_DESCRIPTION_BASE_PROMPT
        assert "{category}" in PRODUCT_DESCRIPTION_BASE_PROMPT
        assert "{brand}" in PRODUCT_DESCRIPTION_BASE_PROMPT
        assert "{additional_info}" in PRODUCT_DESCRIPTION_BASE_PROMPT
        
        # Product suggestions prompt
        assert "{category}" in PRODUCT_SUGGESTIONS_PROMPT
        assert "{count}" in PRODUCT_SUGGESTIONS_PROMPT
        
        # Improve description prompt
        assert "{current_description}" in IMPROVE_DESCRIPTION_PROMPT
    
    def test_prompt_constants_are_strings(self):
        """Test that all prompt constants are strings"""
        assert isinstance(PRODUCT_DESCRIPTION_BASE_PROMPT, str)
        assert isinstance(PRODUCT_SUGGESTIONS_PROMPT, str)
        assert isinstance(IMPROVE_DESCRIPTION_PROMPT, str)
    
    def test_prompt_constants_not_empty(self):
        """Test that prompt constants are not empty"""
        assert len(PRODUCT_DESCRIPTION_BASE_PROMPT.strip()) > 0
        assert len(PRODUCT_SUGGESTIONS_PROMPT.strip()) > 0
        assert len(IMPROVE_DESCRIPTION_PROMPT.strip()) > 0