from src.infrastructure.llm.junior_llm_service import JuniorLLMService
from src.infrastructure.llm.senior_llm_service import SeniorLLMService
import logging

logger = logging.getLogger(__name__)

class ChainValidatorService:
    def __init__(self):
        self.junior = JuniorLLMService()
        self.senior = SeniorLLMService()
    
    def generate_answer(self, question: str, conversation_history: list = None) -> dict:
        logger.info(f"Processing question: {question[:50]}...")
        
        # Junior responde primeiro
        junior_result = self.junior.generate(question, conversation_history)
        
        # Se confidence alta, retorna direto
        if not junior_result["needs_validation"]:
            logger.info(f"High confidence ({junior_result['confidence']}%) - skipping Senior")
            return {
                "content": junior_result["content"],
                "model": "gemini-2.0-flash-lite",
                "used_senior": False
            }
        
        # Se confidence baixa, Senior valida
        logger.info(f"Low confidence ({junior_result['confidence']}%) - calling Senior")
        senior_result = self.senior.validate(question, junior_result["content"], conversation_history)
        
        return {
            "content": senior_result["content"],
            "model": "gemini-2.5-pro",
            "used_senior": True
        }
