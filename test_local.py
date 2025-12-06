"""
Script de teste para verificar se a API está funcionando localmente
"""
import requests
import sys

def test_api():
    base_url = "http://localhost:8000"
    
    print("🔍 Testando FaceCrop API localmente...\n")
    
    # Teste 1: Health check
    print("1. Testando /health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ OK - Status: {response.status_code}")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"   ❌ Erro - Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Erro: Não foi possível conectar ao servidor")
        print("   💡 Certifique-se de que o servidor está rodando: python main.py")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Documentação
    print("\n2. Testando /docs...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ OK - Status: {response.status_code}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Aviso: {e}")
    
    # Teste 3: Endpoint protegido sem API key
    print("\n3. Testando /detect sem API key (deve falhar)...")
    try:
        response = requests.post(f"{base_url}/detect", timeout=5)
        if response.status_code == 401:
            print(f"   ✅ OK - Autenticação funcionando (Status: {response.status_code})")
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Aviso: {e}")
    
    print("\n✅ Todos os testes básicos concluídos!")
    print(f"\n📚 Documentação disponível em: {base_url}/docs")
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)

