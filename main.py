"""
FaceCrop API
API para detecção facial e corte inteligente de vídeo
FastAPI com OpenCV
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Security, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import time

from utils.detector import get_detector
from utils.image_handler import process_uploaded_file, download_image_from_url
from utils.auth import verify_api_key
from utils.security import SecurityMiddleware

# Inicializar FastAPI
app = FastAPI(
    title="FaceCrop API",
    description="API para detectar posição do nariz em frames de vídeo para corte inteligente 9:16",
    version="1.0.0"
)

# Adicionar middleware de segurança (deve vir antes do CORS)
app.add_middleware(SecurityMiddleware)

# Configurar CORS (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos Pydantic
class UrlRequest(BaseModel):
    """Modelo para requisição com URL"""
    url: HttpUrl


class DetectionResponse(BaseModel):
    """Modelo de resposta da detecção"""
    x: float
    y: float
    face_detected: bool
    image_width: int
    image_height: int
    confidence: float
    processing_time_ms: Optional[float] = None


class HealthResponse(BaseModel):
    """Modelo de resposta do health check"""
    status: str


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Endpoint de verificação de saúde da API.
    Não requer autenticação.
    """
    return {"status": "ok"}


@app.post(
    "/detect",
    response_model=DetectionResponse,
    tags=["Detection"],
    summary="Detectar nariz via upload de arquivo",
    description="Recebe uma imagem via upload e retorna as coordenadas do nariz detectado."
)
async def detect_from_upload(
    file: UploadFile = File(...),
    api_key: str = Security(verify_api_key)
):
    """
    Detecta a posição do nariz em uma imagem enviada via upload.
    
    Requer autenticação via header X-API-Key.
    
    Args:
        file: Arquivo de imagem (JPG, PNG ou WEBP)
        api_key: API key validada pelo middleware
        
    Returns:
        DetectionResponse: Coordenadas do nariz e informações da detecção
    """
    start_time = time.time()
    
    try:
        # Processar arquivo enviado
        image_array, width, height = await process_uploaded_file(file)
        
        # Obter detector
        detector = get_detector()
        
        # Detectar nariz
        nose_x, nose_y, face_detected, confidence, img_width, img_height = detector.detect_nose_position(
            image_array
        )
        
        processing_time = (time.time() - start_time) * 1000  # em milissegundos
        
        return DetectionResponse(
            x=round(nose_x, 2),
            y=round(nose_y, 2),
            face_detected=face_detected,
            image_width=img_width,
            image_height=img_height,
            confidence=round(confidence, 2),
            processing_time_ms=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar imagem: {str(e)}"
        )


@app.post(
    "/detect-url",
    response_model=DetectionResponse,
    tags=["Detection"],
    summary="Detectar nariz via URL",
    description="Recebe uma URL de imagem e retorna as coordenadas do nariz detectado."
)
async def detect_from_url(
    request: UrlRequest,
    api_key: str = Security(verify_api_key)
):
    """
    Detecta a posição do nariz em uma imagem baixada de uma URL.
    
    Requer autenticação via header X-API-Key.
    
    Args:
        request: Objeto contendo a URL da imagem
        api_key: API key validada pelo middleware
        
    Returns:
        DetectionResponse: Coordenadas do nariz e informações da detecção
    """
    start_time = time.time()
    
    try:
        # Converter HttpUrl para string
        url_str = str(request.url)
        
        # Baixar e processar imagem
        image_array, width, height = await download_image_from_url(url_str)
        
        # Obter detector
        detector = get_detector()
        
        # Detectar nariz
        nose_x, nose_y, face_detected, confidence, img_width, img_height = detector.detect_nose_position(
            image_array
        )
        
        processing_time = (time.time() - start_time) * 1000  # em milissegundos
        
        return DetectionResponse(
            x=round(nose_x, 2),
            y=round(nose_y, 2),
            face_detected=face_detected,
            image_width=img_width,
            image_height=img_height,
            confidence=round(confidence, 2),
            processing_time_ms=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar imagem: {str(e)}"
        )


# Handler 404 customizado
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Handler customizado para 404 - não expõe informações sobre paths tentados.
    """
    return JSONResponse(
        status_code=404,
        content={"detail": "Not found"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

