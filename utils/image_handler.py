"""
Módulo para manipulação de imagens (upload e download via URL)
"""
import io
import requests
from PIL import Image
import numpy as np
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException, status

# Configurações
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FORMATS = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
URL_TIMEOUT = 5  # segundos


def validate_image_format(content_type: str) -> bool:
    """
    Valida se o formato da imagem é suportado.
    
    Args:
        content_type: MIME type da imagem
        
    Returns:
        bool: True se o formato for válido
    """
    return content_type.lower() in ALLOWED_FORMATS


async def process_uploaded_file(file: UploadFile) -> Tuple[np.ndarray, int, int]:
    """
    Processa arquivo enviado via upload.
    
    Args:
        file: Arquivo enviado via multipart/form-data
        
    Returns:
        Tuple[np.ndarray, int, int]: Imagem em RGB, largura, altura
        
    Raises:
        HTTPException: Se o arquivo for inválido
    """
    # Validar formato
    if not validate_image_format(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato não suportado. Use: JPG, PNG ou WEBP"
        )
    
    # Ler conteúdo
    contents = await file.read()
    
    # Validar tamanho
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo muito grande. Máximo: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    try:
        # Converter para PIL Image
        image = Image.open(io.BytesIO(contents))
        
        # Converter para RGB (MediaPipe requer)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Converter para numpy array
        img_array = np.array(image)
        
        height, width = img_array.shape[:2]
        
        return img_array, width, height
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar imagem: {str(e)}"
        )


def sanitize_url(url: str) -> str:
    """
    Sanitiza URL para evitar SSRF e outros ataques.
    
    Args:
        url: URL a ser sanitizada
        
    Returns:
        str: URL sanitizada
        
    Raises:
        HTTPException: Se a URL for inválida
    """
    if not url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL deve começar com http:// ou https://"
        )
    
    # Bloquear localhost e IPs privados (proteção SSRF)
    blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "::1"]
    from urllib.parse import urlparse
    parsed = urlparse(url)
    
    if any(blocked in parsed.netloc.lower() for blocked in blocked_hosts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URLs locais não são permitidas por segurança"
        )
    
    return url


async def download_image_from_url(url: str) -> Tuple[np.ndarray, int, int]:
    """
    Baixa imagem de uma URL e processa.
    
    Args:
        url: URL da imagem
        
    Returns:
        Tuple[np.ndarray, int, int]: Imagem em RGB, largura, altura
        
    Raises:
        HTTPException: Se houver erro no download ou processamento
    """
    # Sanitizar URL
    sanitized_url = sanitize_url(url)
    
    try:
        # Fazer requisição com timeout
        response = requests.get(
            sanitized_url,
            timeout=URL_TIMEOUT,
            stream=True,
            headers={"User-Agent": "FaceDetectionAPI/1.0"}
        )
        response.raise_for_status()
        
        # Validar content-type
        content_type = response.headers.get("content-type", "").split(";")[0].strip()
        if not validate_image_format(content_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato não suportado na URL. Use: JPG, PNG ou WEBP"
            )
        
        # Ler conteúdo
        contents = response.content
        
        # Validar tamanho
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Imagem muito grande. Máximo: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Converter para PIL Image
        image = Image.open(io.BytesIO(contents))
        
        # Converter para RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Converter para numpy array
        img_array = np.array(image)
        
        height, width = img_array.shape[:2]
        
        return img_array, width, height
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Timeout ao baixar imagem (máximo {URL_TIMEOUT}s)"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao baixar imagem: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar imagem: {str(e)}"
        )

