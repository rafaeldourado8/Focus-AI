"""
Unit tests for identity module

Tests cover:
- Model name mapping
- Log sanitization
- Public name conversion
- Provider mapping
"""

import pytest
from src.infrastructure.identity import (
    sanitize_log,
    get_public_model_name,
    get_provider_model,
    MODEL_JUNIOR,
    MODEL_SENIOR,
    MODEL_DEBUG,
    PRODUCT_NAME,
    FORBIDDEN_TERMS
)


class TestSanitizeLog:
    """Test log sanitization functionality"""
    
    def test_sanitize_removes_google(self):
        message = "Using Google Gemini API"
        result = sanitize_log(message)
        assert "google" not in result.lower()
        assert "***" in result
    
    def test_sanitize_removes_gemini(self):
        message = "Gemini Pro response received"
        result = sanitize_log(message)
        assert "gemini" not in result.lower()
        assert "***" in result
    
    def test_sanitize_removes_openai(self):
        message = "OpenAI GPT-4 called"
        result = sanitize_log(message)
        assert "openai" not in result.lower()
        assert "***" in result
    
    def test_sanitize_preserves_clean_message(self):
        message = "Processing user request"
        result = sanitize_log(message)
        assert result == message
    
    def test_sanitize_handles_multiple_terms(self):
        message = "Google Gemini and OpenAI used"
        result = sanitize_log(message)
        assert "google" not in result.lower()
        assert "gemini" not in result.lower()
        assert "openai" not in result.lower()
    
    def test_sanitize_case_insensitive(self):
        message = "GOOGLE gemini OpenAI"
        result = sanitize_log(message)
        assert "google" not in result.lower()


class TestGetPublicModelName:
    """Test public model name conversion"""
    
    def test_junior_model_name(self):
        result = get_public_model_name(MODEL_JUNIOR)
        assert result == "Cerberus Lite"
    
    def test_senior_model_name(self):
        result = get_public_model_name(MODEL_SENIOR)
        assert result == "Cerberus Pro"
    
    def test_debug_model_name(self):
        result = get_public_model_name(MODEL_DEBUG)
        assert result == "Cerberus Debug"
    
    def test_unknown_model_returns_product_name(self):
        result = get_public_model_name("unknown-model")
        assert result == PRODUCT_NAME


class TestGetProviderModel:
    """Test provider model mapping"""
    
    def test_junior_maps_to_flash(self):
        result = get_provider_model(MODEL_JUNIOR)
        assert "flash" in result.lower()
    
    def test_senior_maps_to_pro(self):
        result = get_provider_model(MODEL_SENIOR)
        assert "pro" in result.lower()
    
    def test_debug_maps_to_pro(self):
        result = get_provider_model(MODEL_DEBUG)
        assert "pro" in result.lower()
    
    def test_unknown_model_returns_default(self):
        result = get_provider_model("unknown")
        assert result is not None


class TestConstants:
    """Test module constants"""
    
    def test_forbidden_terms_not_empty(self):
        assert len(FORBIDDEN_TERMS) > 0
    
    def test_forbidden_terms_lowercase(self):
        for term in FORBIDDEN_TERMS:
            assert term == term.lower()
    
    def test_product_name_defined(self):
        assert PRODUCT_NAME == "Cerberus AI"
    
    def test_model_constants_defined(self):
        assert MODEL_JUNIOR == "cerberus-lite"
        assert MODEL_SENIOR == "cerberus-pro"
        assert MODEL_DEBUG == "cerberus-debug"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_sanitize_empty_string(self):
        result = sanitize_log("")
        assert result == ""
    
    def test_sanitize_none_handling(self):
        # Should raise TypeError for None input
        with pytest.raises(TypeError):
            sanitize_log(None)
    
    def test_get_public_model_empty_string(self):
        result = get_public_model_name("")
        assert result == PRODUCT_NAME
