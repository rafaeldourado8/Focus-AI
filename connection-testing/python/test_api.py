import requests
import json
import os
from typing import Optional, List, Dict
from pathlib import Path

# Carrega .env
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

class CerberusClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.messages: List[Dict] = []
    
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def ask(self, question: str, debug_mode: bool = False):
        self.messages.append({"role": "user", "content": question})
        
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            headers=self._headers(),
            json={
                "model": "cerberus-pro",
                "messages": self.messages,
                "debug_mode": debug_mode
            }
        )
        response.raise_for_status()
        data = response.json()
        
        assistant_msg = data["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": assistant_msg})
        
        return data
    
    def analyze_code(self, code: str, language: str, checks: List[str] = None):
        response = requests.post(
            f"{self.base_url}/v1/code/analyze",
            headers=self._headers(),
            json={
                "code": code,
                "language": language,
                "checks": checks or ["security", "performance", "style"]
            }
        )
        response.raise_for_status()
        return response.json()
    
    def debug_code(self, error: str, code: str, language: str, context: str = None):
        response = requests.post(
            f"{self.base_url}/v1/code/debug",
            headers=self._headers(),
            json={
                "error": error,
                "code": code,
                "language": language,
                "context": context
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_models(self):
        response = requests.get(
            f"{self.base_url}/v1/models",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    API_KEY = os.getenv('CERBERUS_API_KEY', 'your-api-key-here')
    
    if API_KEY == 'your-api-key-here':
        print("❌ Configure CERBERUS_API_KEY no arquivo .env")
        exit(1)
    
    client = CerberusClient(API_KEY)
    
    print("💬 Enviando pergunta...")
    answer = client.ask("Como implementar JWT em FastAPI?")
    print(f"✅ Resposta: {answer['choices'][0]['message']['content'][:100]}...")
    print(f"📊 Tokens: {answer['usage']['total_tokens']}")
    
    print("\n🔍 Listando modelos...")
    models = client.get_models()
    print(f"✅ {len(models['models'])} modelos disponíveis")
