import pytest
from unittest.mock import Mock, patch
from src.infrastructure.llm.chain_validator_service import ChainValidatorService

@pytest.fixture
def chain_service():
    return ChainValidatorService()

def test_high_confidence_skips_senior(chain_service):
    """Testa que confidence alta não chama Senior"""
    with patch.object(chain_service.junior, 'generate') as mock_junior:
        mock_junior.return_value = {
            "response": {"content": "Test", "explanation": "Test", "edge_cases": "N/A"},
            "confidence": 85,
            "needs_validation": False
        }
        
        result = chain_service.generate_socratic_answer("Simple question")
        
        assert result["metadata"]["used_senior"] == False
        assert result["metadata"]["confidence"] == 85
        assert result["metadata"]["model"] == "gemini-2.0-flash-lite"

def test_low_confidence_calls_senior(chain_service):
    """Testa que confidence baixa chama Senior"""
    with patch.object(chain_service.junior, 'generate') as mock_junior, \
         patch.object(chain_service.senior, 'validate') as mock_senior:
        
        mock_junior.return_value = {
            "response": {"content": "Test", "explanation": "Test", "edge_cases": "N/A"},
            "confidence": 50,
            "needs_validation": True
        }
        
        mock_senior.return_value = {
            "validated": True,
            "corrections": "Improved",
            "final_response": {"content": "Better", "explanation": "Better", "edge_cases": "N/A"}
        }
        
        result = chain_service.generate_socratic_answer("Complex question")
        
        assert result["metadata"]["used_senior"] == True
        assert result["metadata"]["confidence"] == 50
        assert "corrections" in result["metadata"]

def test_chain_returns_standard_format(chain_service):
    """Testa que Chain sempre retorna formato padrão"""
    with patch.object(chain_service.junior, 'generate') as mock_junior:
        mock_junior.return_value = {
            "response": {"content": "A", "explanation": "B", "edge_cases": "C"},
            "confidence": 90,
            "needs_validation": False
        }
        
        result = chain_service.generate_socratic_answer("Test")
        
        assert "content" in result
        assert "explanation" in result
        assert "edge_cases" in result
        assert "metadata" in result
