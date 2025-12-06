"""
Módulo de segurança e middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import re


# Lista de paths suspeitos que devem ser bloqueados (apenas arquivos, não paths da API)
SUSPICIOUS_PATHS = [
    r'\.env$',
    r'\.git/',
    r'\.git$',
    r'\.ssh/',
    r'\.htaccess$',
    r'\.htpasswd$',
    r'\.config$',
    r'\.secret$',
    r'\.key$',
    r'\.pem$',
    r'\.crt$',
    r'\.ini$',
    r'\.conf$',
    r'\.log$',
    r'\.sql$',
    r'\.db$',
    r'\.sqlite$',
    r'\.dump$',
    r'\.backup$',
    r'\.bak$',
    r'\.old$',
    r'\.swp$',
    r'\.swo$',
    r'\.tmp$',
    r'\.temp$',
    r'\.php$',
    r'\.asp$',
    r'\.aspx$',
    r'\.jsp$',
    r'\.sh$',
    r'\.bat$',
    r'\.cmd$',
    r'\.exe$',
    r'\.dll$',
    r'\.so$',
    r'\.dylib$',
    r'\.pyc$',
    r'\.pyo$',
    r'\.pyd$',
    r'\.class$',
    r'\.jar$',
    r'\.war$',
    r'\.ear$',
    r'\.zip$',
    r'\.tar$',
    r'\.gz$',
    r'\.bz2$',
    r'\.7z$',
    r'\.rar$',
    r'\.apk$',
    r'\.ipa$',
    r'\.deb$',
    r'\.rpm$',
    r'\.msi$',
    r'\.dmg$',
    r'\.iso$',
    r'\.img$',
    r'\.bin$',
    r'\.run$',
    r'\.ps1$',
    r'\.vbs$',
    r'\.gitignore$',
    r'\.gitattributes$',
    r'\.gitmodules$',
    r'\.gitconfig$',
    r'\.gitkeep$',
    r'\.dockerignore$',
    r'\.dockerfile$',
]


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware de segurança para bloquear tentativas de acesso a arquivos sensíveis.
    """
    
    def __init__(self, app):
        super().__init__(app)
        # Compilar padrões regex uma vez
        self.suspicious_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in SUSPICIOUS_PATHS]
    
    async def dispatch(self, request: Request, call_next):
        # Verificar se o path contém padrões suspeitos
        path = request.url.path
        
        # Lista de paths válidos da API que não devem ser bloqueados
        # Inclui todos os recursos do Swagger UI e ReDoc
        valid_api_paths = [
            '/health',
            '/docs',
            '/redoc',
            '/openapi.json',
            '/detect',
            '/detect-url',
            '/static',  # Recursos estáticos do Swagger
        ]
        
        # Se for um path válido da API ou recurso do Swagger, permitir imediatamente
        if any(path.startswith(valid) for valid in valid_api_paths):
            response = await call_next(request)
            return response
        
        # Verificar path traversal (mas permitir /docs e recursos do Swagger)
        if '..' in path:
            # Permitir apenas se for parte de um path válido da API
            if not any(valid in path for valid in valid_api_paths):
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "Not found"}
                )
        
        # Verificar se começa com ponto (exceto paths válidos)
        if path.startswith('/.') and path not in ['/docs', '/redoc'] and not path.startswith('/docs') and not path.startswith('/redoc'):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Not found"}
            )
        
        # Verificar padrões suspeitos (apenas para arquivos, não paths da API)
        for pattern in self.suspicious_patterns:
            if pattern.search(path):
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "Not found"}
                )
        
        # Continuar com a requisição
        response = await call_next(request)
        return response
