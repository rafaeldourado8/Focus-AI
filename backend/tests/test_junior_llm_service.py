import pytest
from unittest.mock import Mock, patch
from src.infrastructure.llm.junior_llm_service import JuniorLLMService

@pytest.fixture
def junior_service():
    return JuniorLLMService()

def test_generate_returns_confidence(junior_service):
    """Testa se Junior retorna confidence score"""
    with patch.object(junior_service.client, 'chat') as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': '{"content": "Test", "explanation": "Test", "edge_cases": "N/A", "confidence": 85}'
            }
        }
        
        result = junior_service.generate("What is Python?")
        
        assert "confidence" in result
        assert result["confidence"] == 85
        assert "needs_validation" in result
        assert result["needs_validation"] == False

def test_generate_low_confidence_needs_validation(junior_service):
    """Testa se confidence baixa marca needs_validation=True"""
    with patch.object(junior_service.client, 'chat') as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': '{"content": "Test", "explanation": "Test", "edge_cases": "N/A", "confidence": 50}'
            }
        }
        
        result = junior_service.generate("Complex question")
        
        assert result["confidence"] == 50
        assert result["needs_validation"] == True

def test_generate_handles_error(junior_service):
    """Testa fallback quando Junior falha"""
    with patch.object(junior_service.client, 'chat', side_effect=Exception("Connection error")):
        result = junior_service.generate("Test")
        
        assert result["confidence"] == 0
        assert result["needs_validation"] == True
        assert "Erro" in result["response"]["content"]
