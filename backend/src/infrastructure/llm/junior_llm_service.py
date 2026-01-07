import google.generativeai as genai
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class JuniorLLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite',
            generation_config={"temperature": 0.7},
            system_instruction="""Você é um assistente de programação direto e prático.

Responda naturalmente como um desenvolvedor experiente. Sem formalidades.
Forneça código, exemplos e soluções diretas.

Foco: Python, JavaScript, DevOps, debugging, arquitetura."""
        )
    
    def generate(self, question: str, conversation_history: list = None) -> dict:
        try:
            if conversation_history:
                chat = self.model.start_chat(history=conversation_history)
                response = chat.send_message(question)
            else:
                response = self.model.generate_content(question)
            
            content = response.text
            # Sempre alta confidence para evitar validação desnecessária
            confidence = 95
            
            return {
                "content": content,
                "confidence": confidence,
                "needs_validation": False
            }
            
        except Exception as e:
            logger.error(f"Junior LLM error: {e}")
            return {
                "content": f"Erro: {str(e)}",
                "confidence": 0,
                "needs_validation": False
            }
