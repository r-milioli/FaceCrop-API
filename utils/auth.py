"""
Módulo de autenticação por API Key
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Header esperado para API Key
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# API Key válida (pode ser configurada via variável de ambiente ou arquivo)
def get_api_key():
    """
    Obtém a API key de variável de ambiente ou arquivo (Docker Secrets).
    Prioridade: API_KEY > API_KEY_FILE > default
    """
    # Tentar variável de ambiente primeiro
    api_key = os.getenv("API_KEY")
    if api_key:
        return api_key
    
    # Tentar ler de arquivo (Docker Secrets)
    api_key_file = os.getenv("API_KEY_FILE")
    if api_key_file and os.path.exists(api_key_file):
        try:
            with open(api_key_file, 'r') as f:
                return f.read().strip()
        except Exception:
            pass
    
    # Fallback para default
    return os.getenv("API_KEY", "default-api-key-change-me")

VALID_API_KEY = get_api_key()


async def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
    """
    Verifica se a API key fornecida é válida.
    
    Args:
        api_key: API key extraída do header X-API-Key
        
    Returns:
        str: A API key se for válida
        
    Raises:
        HTTPException: Se a API key estiver ausente ou inválida
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key ausente. Forneça o header X-API-Key."
        )
    
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key inválida."
        )
    
    return api_key

