# FaceCrop API

API leve desenvolvida em Python com FastAPI que detecta a posição do nariz do falante em frames de vídeo para realizar corte inteligente no formato 9:16.

## 🚀 Características

- **Detecção facial** usando OpenCV Headless (compatível com Python 3.13+)
- **Autenticação por API Key** para segurança
- **Middleware de segurança** para proteção contra exploração
- **Suporte a múltiplas faces** (seleciona a maior automaticamente)
- **Dois métodos de entrada**: upload de arquivo ou URL
- **Processamento assíncrono** com FastAPI
- **Documentação automática** (Swagger UI e ReDoc)
- **Pronto para Docker** com suporte a Docker Swarm

## 📋 Requisitos

- Python 3.9+ (testado com Python 3.13)
- pip

## 🔧 Instalação

1. Clone o repositório ou navegue até o diretório do projeto

2. Crie um ambiente virtual (recomendado):

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Configure a API Key:

   - **Windows**: `copy env.example .env`
   - **Linux/Mac**: `cp env.example .env`

   Edite o arquivo `.env` e defina uma API key segura:

```env
API_KEY=sua-api-key-secreta-aqui
```

## 🏃 Execução

Inicie o servidor:

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa (Swagger): `http://localhost:8000/docs`

### Teste Rápido

Execute o script de teste para verificar se tudo está funcionando:

```bash
python test_local.py
```

## 📡 Endpoints

### `GET /health`

Verifica o status da API (não requer autenticação).

**Resposta:**

```json
{
  "status": "ok"
}
```

### `POST /detect`

Detecta nariz via upload de arquivo.

**Headers:**

```
X-API-Key: sua-api-key-aqui
Content-Type: multipart/form-data
```

**Body:**

- `file`: Arquivo de imagem (JPG, PNG ou WEBP)

**Resposta:**

```json
{
  "x": 960.5,
  "y": 540.2,
  "face_detected": true,
  "image_width": 1920,
  "image_height": 1080,
  "confidence": 0.95,
  "processing_time_ms": 245.3
}
```

### `POST /detect-url`

Detecta nariz via URL da imagem.

**Headers:**

```
X-API-Key: sua-api-key-aqui
Content-Type: application/json
```

**Body:**

```json
{
  "url": "https://exemplo.com/imagem.jpg"
}
```

**Resposta:**

```json
{
  "x": 960.5,
  "y": 540.2,
  "face_detected": true,
  "image_width": 1920,
  "image_height": 1080,
  "confidence": 0.95,
  "processing_time_ms": 312.7
}
```

## 🔐 Autenticação

Todos os endpoints de detecção (`/detect` e `/detect-url`) requerem autenticação via header `X-API-Key`.

Configure sua API key no arquivo `.env`:

```env
API_KEY=sua-chave-secreta
```

A API key também pode ser configurada via:
- Variável de ambiente `API_KEY` (produção)
- Arquivo via `API_KEY_FILE` (Docker Secrets)

## 📝 Exemplo de Uso

### cURL - Upload de arquivo

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "X-API-Key: sua-api-key-aqui" \
  -F "file=@imagem.jpg"
```

### cURL - Via URL

```bash
curl -X POST "http://localhost:8000/detect-url" \
  -H "X-API-Key: sua-api-key-aqui" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com/imagem.jpg"}'
```

### Python

```python
import requests

url = "http://localhost:8000/detect"
headers = {"X-API-Key": "sua-api-key-aqui"}
files = {"file": open("imagem.jpg", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

## 🐳 Docker

### Imagem Docker Hub

A imagem está disponível no Docker Hub: `automacaodebaixocusto/facecrop-api`

```bash
docker pull automacaodebaixocusto/facecrop-api:latest
```

### Build da Imagem

#### Build Local

```bash
docker build -t automacaodebaixocusto/facecrop-api:latest .
```

#### Build e Push para Docker Hub

**Linux/Mac:**
```bash
chmod +x build-and-push.sh
./build-and-push.sh
```

**Windows (PowerShell):**
```powershell
.\build-and-push.ps1
```

Ou manualmente:
```bash
docker build -t automacaodebaixocusto/facecrop-api:latest .
docker push automacaodebaixocusto/facecrop-api:latest
```

### Executar com Docker Compose

```bash
# Criar arquivo .env com sua API_KEY
echo "API_KEY=sua-chave-secreta" > .env

# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Deploy em Docker Swarm

1. **Inicializar Swarm (se ainda não estiver inicializado):**
```bash
docker swarm init
```

2. **Criar secret para API_KEY (opcional, mais seguro):**
```bash
echo "sua-chave-secreta" | docker secret create api_key -
```

3. **Deploy do stack:**
```bash
# Exportar API_KEY como variável de ambiente
export API_KEY=sua-chave-secreta

# Deploy
docker stack deploy -c docker-stack.yml facecrop

# Verificar status
docker stack services facecrop

# Ver logs
docker service logs facecrop_facecrop-api

# Remover stack
docker stack rm facecrop
```

**Para usar Docker Secrets**, use `docker-stack-secrets.yml`:

```bash
docker stack deploy -c docker-stack-secrets.yml facecrop
```

### Variáveis de Ambiente

A API key pode ser configurada via:
- Arquivo `.env` (desenvolvimento)
- Variável de ambiente `API_KEY` (produção)
- Docker secrets (Docker Swarm - mais seguro)

## 📊 Casos de Uso

✅ **1 pessoa falando**: Detecta face única e retorna posição do nariz  
✅ **Múltiplas pessoas**: Seleciona a maior face e retorna seu nariz  
✅ **Nenhuma face**: Retorna centro da imagem como fallback  
✅ **Upload ou URL**: Suporta ambos os métodos de entrada

## ⚙️ Configurações

- **Tamanho máximo de arquivo**: 10MB
- **Timeout de URL**: 5 segundos
- **Formatos suportados**: JPG, PNG, WEBP
- **Tempo de resposta esperado**: < 500ms

## 🔒 Segurança

- **Autenticação por API Key** obrigatória para endpoints de detecção
- **Middleware de segurança** que bloqueia tentativas de acesso a arquivos sensíveis
- **Validação de formato de arquivo** (apenas imagens permitidas)
- **Sanitização de URLs** (proteção SSRF)
- **Limite de tamanho de upload** (10MB)
- **Timeout para downloads** (5 segundos)
- **Handler 404 customizado** que não expõe informações sensíveis
- **Proteção contra path traversal** e exploração de diretórios

### Middleware de Segurança

O middleware bloqueia automaticamente tentativas de acesso a:
- Arquivos de configuração (`.env`, `.config`, etc.)
- Arquivos do Git (`.git`, `.gitignore`, etc.)
- Arquivos de sistema e temporários
- Scripts executáveis

## 📚 Documentação

Acesse a documentação interativa em:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🛠️ Estrutura do Projeto

```
facecrop-api/
├── main.py                  # Aplicação FastAPI
├── requirements.txt         # Dependências
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Compose para desenvolvimento
├── docker-stack.yml        # Stack para Docker Swarm
├── docker-stack-secrets.yml # Stack com Docker Secrets
├── .dockerignore           # Arquivos ignorados no build
├── build-and-push.sh       # Script de build (Linux/Mac)
├── build-and-push.ps1      # Script de build (Windows)
├── test_local.py           # Script de teste local
├── .env                    # Configurações (não versionado)
├── env.example             # Exemplo de configuração
├── README.md               # Este arquivo
├── DEPLOY.md               # Guia de deploy
├── TROUBLESHOOTING.md      # Guia de troubleshooting
├── NOTA_MEDIAPIPE.md       # Nota sobre MediaPipe
└── utils/
    ├── auth.py             # Autenticação por API Key
    ├── detector.py         # Lógica OpenCV
    ├── image_handler.py    # Download/Upload
    └── security.py         # Middleware de segurança
```

## 🐛 Troubleshooting

Se encontrar problemas, consulte o arquivo `TROUBLESHOOTING.md` para soluções comuns.

### Problemas Comuns

1. **Erro ao iniciar**: Verifique se todas as dependências estão instaladas
2. **Porta em uso**: Use outra porta ou pare o processo que está usando a porta 8000
3. **Erro 401**: Verifique se o arquivo `.env` existe e contém `API_KEY`
4. **Erro com OpenCV**: Certifique-se de usar `opencv-python-headless` (já incluído)

Execute o script de teste para diagnóstico:

```bash
python test_local.py
```

## 📦 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **OpenCV Headless** - Processamento de imagens sem dependências gráficas
- **Uvicorn** - Servidor ASGI de alta performance
- **Pillow** - Manipulação de imagens
- **Pydantic** - Validação de dados
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 📄 Licença

Este projeto é open-source e está disponível para uso livre.

## 🔗 Links Úteis

- **Docker Hub**: `automacaodebaixocusto/facecrop-api`
- **Documentação FastAPI**: https://fastapi.tiangolo.com
- **Documentação OpenCV**: https://docs.opencv.org
