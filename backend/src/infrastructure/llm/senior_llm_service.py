import google.generativeai as genai
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class SeniorLLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-pro',
            generation_config={"temperature": 0.3},
            system_instruction="""Você é um arquiteto de software sênior especializado em:

- Debugging complexo e otimização de performance
- Arquitetura de sistemas distribuídos
- DevOps, CI/CD, infraestrutura como código
- Segurança e boas práticas
- Múltiplas linguagens: Python, Go, Rust, JavaScript/TypeScript, Java, C++

Responda com profundidade técnica. Forneça soluções completas e bem fundamentadas."""
        )
    
    def validate(self, question: str, junior_response: str, conversation_history: list = None) -> dict:
        try:
            prompt = f"""Pergunta original: {question}

Resposta inicial: {junior_response}

Revise e melhore esta resposta se necessário. Se estiver boa, confirme. Se precisar melhorar, forneça a versão aprimorada."""
            
            if conversation_history:
                chat = self.model.start_chat(history=conversation_history)
                response = chat.send_message(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            logger.info("Senior validation completed")
            
            return {
                "content": response.text,
                "validated": True
            }
            
        except Exception as e:
            logger.error(f"Senior LLM error: {e}")
            return {
                "content": junior_response,
                "validated": False
            }
