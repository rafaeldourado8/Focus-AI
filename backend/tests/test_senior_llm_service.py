import pytest
from unittest.mock import Mock, patch
from src.infrastructure.llm.senior_llm_service import SeniorLLMService

@pytest.fixture
def senior_service():
    return SeniorLLMService()

def test_validate_corrects_response(senior_service):
    """Testa se Senior valida e corrige resposta"""
    junior_response = {
        "content": "Python is a language",
        "explanation": "Basic explanation",
        "edge_cases": "N/A"
    }
    
    with patch.object(senior_service.model, 'generate_content') as mock_gen:
        mock_gen.return_value.text = '''{
            "validated": true,
            "corrections": "Added more details",
            "final_response": {
                "content": "Python is a high-level programming language",
                "explanation": "Detailed explanation",
                "edge_cases": "Performance considerations"
            }
        }'''
        
        result = senior_service.validate("What is Python?", junior_response)
        
        assert result["validated"] == True
        assert "corrections" in result
        assert result["final_response"]["content"] != junior_response["content"]

def test_validate_handles_error(senior_service):
    """Testa fallback quando Senior falha"""
    junior_response = {"content": "Test", "explanation": "Test", "edge_cases": "N/A"}
    
    with patch.object(senior_service.model, 'generate_content', side_effect=Exception("API error")):
        result = senior_service.validate("Test", junior_response)
        
        assert result["validated"] == False
        assert "Erro" in result["corrections"]
        assert result["final_response"] == junior_response
