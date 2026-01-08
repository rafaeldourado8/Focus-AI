"""
Script para criar API Key de teste
"""
import sys
sys.path.append('../../backend/src')

from src.infrastructure.database.connection import get_db
from src.infrastructure.database.api_key_repository import APIKeyRepository
from src.domain.api_key import APIKey

def create_test_key():
    db = next(get_db())
    repo = APIKeyRepository(db)
    
    # Cria API key de teste
    api_key = APIKey(
        user_id="test-user",
        name="Test Key",
        plan="pro"
    )
    
    created = repo.create(api_key)
    
    print("✅ API Key criada com sucesso!")
    print(f"🔑 Key: {created.key}")
    print(f"📦 Plan: {created.plan}")
    print(f"⚡ Rate Limit: {created.get_rate_limit()}/min")
    print(f"\n💡 Use esta key nos testes:")
    print(f'   API_KEY = "{created.key}"')
    
    return created.key

if __name__ == "__main__":
    create_test_key()
