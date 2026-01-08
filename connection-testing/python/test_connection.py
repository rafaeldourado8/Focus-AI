"""
Teste simplificado - usa endpoint /models que não precisa de autenticação
"""
import requests

BASE_URL = "http://localhost:8000"

print("🔍 Testando conectividade...")

# 1. Health check
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health: {response.json()}")
except Exception as e:
    print(f"❌ Health check falhou: {e}")
    exit(1)

# 2. Root endpoint
try:
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✅ API: {data['name']} v{data['version']}")
except Exception as e:
    print(f"❌ Root endpoint falhou: {e}")

print("\n📝 Para testar endpoints autenticados:")
print("1. Crie uma API key no dashboard: http://localhost:3000")
print("2. Ou use o script: python create_api_key.py")
print("3. Atualize API_KEY em test_api.py")
print("4. Execute: python test_api.py")
