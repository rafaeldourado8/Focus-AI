from src.infrastructure.llm.junior_llm_service import JuniorLLMService
from src.infrastructure.llm.senior_llm_service import SeniorLLMService
from src.infrastructure.identity import (
    MODEL_JUNIOR, MODEL_SENIOR, MODEL_DEBUG,
    get_public_model_name, sanitize_log
)
import logging

logger = logging.getLogger(__name__)

class ChainValidatorService:
    def __init__(self):
        self.junior = JuniorLLMService()
        self.senior = SeniorLLMService()
    
    def generate_answer(self, question: str, conversation_history: list = None, debug_mode: bool = False) -> dict:
        logger.info(sanitize_log(f"Processing question: {question[:50]}... [DEBUG={debug_mode}]"))
        
        # Debug Mode: Sempre usa Senior com prompt especializado
        if debug_mode:
            logger.info("Debug Mode activated - using Senior directly")
            senior_result = self.senior.generate_debug(question, conversation_history)
            return {
                "content": senior_result["content"],
                "model": get_public_model_name(MODEL_DEBUG),
                "used_senior": True
            }
        
        # Junior responde primeiro
        junior_result = self.junior.generate(question, conversation_history)
        
        # Se confidence alta, retorna direto
        if not junior_result["needs_validation"]:
            logger.info(f"High confidence ({junior_result['confidence']}%) - skipping Senior")
            return {
                "content": junior_result["content"],
                "model": get_public_model_name(MODEL_JUNIOR),
                "used_senior": False
            }
        
        # Se confidence baixa, Senior valida
        logger.info(f"Low confidence ({junior_result['confidence']}%) - calling Senior")
        senior_result = self.senior.validate(question, junior_result["content"], conversation_history)
        
        return {
            "content": senior_result["content"],
            "model": get_public_model_name(MODEL_SENIOR),
            "used_senior": True
        }
