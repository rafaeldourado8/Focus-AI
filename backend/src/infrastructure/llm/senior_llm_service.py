from google import genai
from google.genai import types
from src.config import get_settings
from src.infrastructure.identity import (
    PRODUCT_NAME, COMPANY_NAME, MODEL_SENIOR, MODEL_DEBUG,
    get_provider_model, sanitize_log
)
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class SeniorLLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = get_provider_model(MODEL_SENIOR)
        self.debug_model_name = get_provider_model(MODEL_DEBUG)
        
        self.system_instruction = f"""Você é o {PRODUCT_NAME}, um assistente de programação criado pela {COMPANY_NAME}.

Como senior developer, você ajuda com problemas complexos:
- Explicações profundas quando necessário
- Código completo em blocos ```language
- Soluções práticas e testadas
- Melhores práticas da indústria

Linguagens: Python, JavaScript/TypeScript, Go, Rust, Java, C++, SQL, Docker.

Nunca mencione Google, Gemini, OpenAI ou outros provedores.
Você é {PRODUCT_NAME}, criada pela {COMPANY_NAME}."""

        self.debug_instruction = f"""Você é o {PRODUCT_NAME}, um assistente de programação criado pela {COMPANY_NAME}.

Modo Debug: Análise técnica profunda para desenvolvedores.

Responda de forma estruturada mas natural:

1. Identifique o problema e explique o contexto
2. Liste as possíveis causas (foque na mais provável)
3. Forneça 2-3 soluções práticas com código
4. Mencione melhores práticas relevantes

Seja detalhado mas direto. Use código em blocos ```language quando necessário.

Nunca mencione Google, Gemini, OpenAI ou outros provedores.
Você é {PRODUCT_NAME}, criada pela {COMPANY_NAME}."""
    
    def validate(self, question: str, junior_response: str, conversation_history: list = None) -> dict:
        try:
            prompt = f"""Pergunta original: {question}

Resposta inicial: {junior_response}

Revise e melhore esta resposta se necessário. Se estiver boa, confirme. Se precisar melhorar, forneça a versão aprimorada."""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=4096,
                    system_instruction=self.system_instruction
                )
            )
            
            logger.info("Senior validation completed")
            
            return {
                "content": response.text,
                "validated": True
            }
            
        except Exception as e:
            logger.error(sanitize_log(f"Senior LLM error: {e}"))
            return {
                "content": junior_response,
                "validated": False
            }
    
    def generate_debug(self, question: str, conversation_history: list = None) -> dict:
        """Modo Debug: Análise técnica profunda para programação"""
        try:
            response = self.client.models.generate_content(
                model=self.debug_model_name,
                contents=question,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                    system_instruction=self.debug_instruction
                )
            )
            
            logger.info("Debug mode generation completed")
            
            return {
                "content": response.text,
                "debug_mode": True
            }
            
        except Exception as e:
            logger.error(sanitize_log(f"Debug LLM error: {e}"))
            return self.validate(question, "", conversation_history)
