import google.generativeai as genai
from src.config import get_settings
import json

# Carrega as configurações globais (incluindo GEMINI_API_KEY)
settings = get_settings()

class LLMService:
    def __init__(self):
        """
        Inicializa o serviço do Google Gemini.
        Nota: Apesar do nome do arquivo ser 'openai_service.py', 
        o projeto foi atualizado para utilizar o Google Generative AI.
        """
        # Configura a chave de API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.7
            }
        )
    
    def generate_socratic_answer(self, question: str) -> dict:
        """
        Gera uma resposta no estilo mentor socrático.
        Solicita explicitamente um JSON para manter a consistência com o frontend.
        """
        prompt = f"""Você é um mentor de tecnologia socrático. 
        Sua missão é guiar o aluno através da pergunta, fornecendo contexto e pontos de reflexão.
        
        Pergunta do aluno: {question}
        
        Responda obrigatoriamente neste formato JSON:
        {{
          "content": "A resposta principal ou uma pergunta guia",
          "explanation": "Uma explicação técnica ou teórica detalhada",
          "edge_cases": "Casos de borda, erros comuns ou exceções sobre o assunto"
        }}"""

        try:
            # Chama a API para gerar o conteúdo
            response = self.model.generate_content(prompt)
            
            # Validação: Garante que o texto retornado é um JSON válido
            return json.loads(response.text)
            
        except Exception as e:
            # Fallback em caso de erro de conexão, quota ou parsing de JSON
            return {
                "content": "Desculpe, ocorreu um erro ao processar sua pergunta com a IA.",
                "explanation": f"Detalhes do erro: {str(e)}",
                "edge_cases": "N/A"
            }