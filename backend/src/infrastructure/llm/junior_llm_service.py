from google import genai
from google.genai import types
from src.config import get_settings
from src.infrastructure.identity import (
    PRODUCT_NAME, COMPANY_NAME, MODEL_JUNIOR,
    get_provider_model, sanitize_log
)
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class JuniorLLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = get_provider_model(MODEL_JUNIOR)
        self.system_instruction = f"""Você é o {PRODUCT_NAME}, um assistente de programação criado pela {COMPANY_NAME}.

Responda de forma natural e direta como um desenvolvedor experiente:
- Seja conversacional e amigável
- Use código quando necessário (blocos ```language)
- Explique de forma clara sem excesso de formatação
- Vá direto ao ponto

Foco: Python, JavaScript, React, Node, DevOps, debugging.

Nunca mencione Google, Gemini, OpenAI ou outros provedores.
Você é {PRODUCT_NAME}, criada pela {COMPANY_NAME}."""
    
    def generate(self, question: str, conversation_history: list = None, language: str = "pt-BR") -> dict:
        try:
            # Mapeia idioma para instrução
            lang_instruction = {
                "pt-BR": "Responda em Português do Brasil.",
                "en-US": "Answer in English.",
                "es-ES": "Responde en Español."
            }.get(language, "Responda em Português do Brasil.")
            
            system_with_lang = f"{self.system_instruction}\n\n{lang_instruction}"
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=question,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                    system_instruction=system_with_lang
                )
            )
            
            content = response.text
            confidence = 95
            
            return {
                "content": content,
                "confidence": confidence,
                "needs_validation": False
            }
            
        except Exception as e:
            logger.error(sanitize_log(f"Junior LLM error: {e}"))
            return {
                "content": f"Erro: {str(e)}",
                "confidence": 0,
                "needs_validation": False
            }
