import pytest
from unittest.mock import Mock, patch
from src.infrastructure.llm.chain_validator_service import ChainValidatorService

class TestDebugMode:
    """Testes para o Debug Mode"""
    
    @pytest.fixture
    def chain_validator(self):
        return ChainValidatorService()
    
    def test_debug_mode_uses_senior_directly(self, chain_validator):
        """Debug Mode deve usar Senior LLM diretamente"""
        with patch.object(chain_validator.senior, 'generate_debug') as mock_debug:
            mock_debug.return_value = {
                "content": "Análise técnica profunda...",
                "debug_mode": True
            }
            
            result = chain_validator.generate_answer(
                "Por que meu código dá erro?",
                debug_mode=True
            )
            
            # Verifica que Senior foi chamado
            mock_debug.assert_called_once()
            
            # Verifica resposta
            assert result["model"] == "gemini-2.5-pro-debug"
            assert result["used_senior"] is True
            assert "Análise técnica profunda" in result["content"]
    
    def test_normal_mode_uses_junior_first(self, chain_validator):
        """Modo normal deve usar Junior primeiro"""
        with patch.object(chain_validator.junior, 'generate') as mock_junior:
            mock_junior.return_value = {
                "content": "Resposta rápida",
                "confidence": 95,
                "needs_validation": False
            }
            
            result = chain_validator.generate_answer(
                "O que é Python?",
                debug_mode=False
            )
            
            # Verifica que Junior foi chamado
            mock_junior.assert_called_once()
            
            # Verifica resposta
            assert result["model"] == "gemini-2.0-flash-lite"
            assert result["used_senior"] is False
    
    def test_debug_mode_prompt_structure(self, chain_validator):
        """Debug Mode deve ter prompt estruturado"""
        with patch.object(chain_validator.senior, 'generate_debug') as mock_debug:
            mock_debug.return_value = {
                "content": "# 🔍 ANÁLISE DETALHADA\n...",
                "debug_mode": True
            }
            
            question = "Como otimizar esta query SQL?"
            result = chain_validator.generate_answer(question, debug_mode=True)
            
            # Verifica que foi chamado com a pergunta
            call_args = mock_debug.call_args
            assert question in str(call_args)
    
    def test_debug_mode_fallback_on_error(self, chain_validator):
        """Debug Mode deve ter fallback em caso de erro"""
        with patch.object(chain_validator.senior, 'generate_debug') as mock_debug:
            # Simula erro
            mock_debug.side_effect = Exception("API Error")
            
            # Deve retornar algo mesmo com erro
            result = chain_validator.generate_answer(
                "Test question",
                debug_mode=True
            )
            
            # Verifica que não quebrou
            assert "content" in result
            assert result["used_senior"] is True


class TestDebugModeIntegration:
    """Testes de integração do Debug Mode"""
    
    def test_debug_mode_end_to_end(self):
        """Teste completo do fluxo de Debug Mode"""
        from src.application.use_cases.ask_question import AskQuestionUseCase
        from unittest.mock import Mock
        
        # Mocks
        session_repo = Mock()
        question_repo = Mock()
        answer_repo = Mock()
        cache_service = Mock()
        llm_service = Mock()
        
        # Configura mocks
        session_repo.get_by_id.return_value = Mock(user_id="user123", status="active")
        cache_service.is_locked.return_value = False
        cache_service.acquire_lock.return_value = True
        cache_service.get_cached_answer.return_value = None
        
        question_repo.create.return_value = Mock(id="q123")
        answer_repo.create.return_value = Mock(id="a123", content="Debug response")
        
        llm_service.generate_answer.return_value = {
            "content": "🔍 ANÁLISE DETALHADA\n...",
            "model": "gemini-2.5-pro-debug",
            "used_senior": True
        }
        
        # Executa use case
        use_case = AskQuestionUseCase(
            session_repo,
            question_repo,
            answer_repo,
            cache_service,
            llm_service
        )
        
        result = use_case.execute(
            "session123",
            "user123",
            "Como debugar memory leak?",
            debug_mode=True
        )
        
        # Verifica que LLM foi chamado com debug_mode=True
        llm_service.generate_answer.assert_called_once()
        call_kwargs = llm_service.generate_answer.call_args[1]
        assert call_kwargs.get("debug_mode") is True
        
        # Verifica resposta
        assert result["used_senior"] is True
        assert result["model"] == "gemini-2.5-pro-debug"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
