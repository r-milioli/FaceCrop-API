# Guia de Deploy - FaceCrop API

Este guia explica como fazer o build e deploy da FaceCrop API no Docker Hub e Docker Swarm.

## 📦 Build e Push para Docker Hub

### Pré-requisitos

1. Ter Docker instalado
2. Estar logado no Docker Hub:
```bash
docker login
```

### Build Local

```bash
docker build -t automacaodebaixocusto/facecrop-api:latest .
```

### Build e Push Automático

**Linux/Mac:**
```bash
chmod +x build-and-push.sh
./build-and-push.sh
```

**Windows (PowerShell):**
```powershell
.\build-and-push.ps1
```

### Build com Tag Específica

```bash
# Build
docker build -t automacaodebaixocusto/facecrop-api:v1.0.0 .

# Push
docker push automacaodebaixocusto/facecrop-api:v1.0.0
```

## 🚀 Deploy em Docker Swarm

### 1. Inicializar Swarm (se necessário)

```bash
docker swarm init
```

### 2. Configurar API Key

**Opção A: Variável de Ambiente (Simples)**
```bash
export API_KEY=sua-chave-secreta-aqui
```

**Opção B: Docker Secret (Recomendado para Produção)**
```bash
echo "sua-chave-secreta-aqui" | docker secret create api_key -
```

Se usar Docker Secret, atualize o `docker-stack.yml` para usar:
```yaml
secrets:
  - api_key
```

E no serviço:
```yaml
environment:
  - API_KEY_FILE=/run/secrets/api_key
```

### 3. Deploy do Stack

```bash
docker stack deploy -c docker-stack.yml facecrop
```

### 4. Verificar Status

```bash
# Listar serviços
docker stack services facecrop

# Ver logs
docker service logs facecrop_facecrop-api -f

# Ver detalhes do serviço
docker service ps facecrop_facecrop-api
```

### 5. Atualizar Stack

```bash
# Fazer pull da nova imagem
docker service update --image automacaodebaixocusto/facecrop-api:latest facecrop_facecrop-api

# Ou recriar o stack
docker stack rm facecrop
docker stack deploy -c docker-stack.yml facecrop
```

### 6. Remover Stack

```bash
docker stack rm facecrop
```

## 🔧 Configurações Avançadas

### Escalar o Serviço

```bash
docker service scale facecrop_facecrop-api=3
```

### Configurar Porta Diferente

Edite o `docker-stack.yml`:
```yaml
ports:
  - "8080:8000"  # Porta externa:porta interna
```

### Adicionar Labels para Placement

No `docker-stack.yml`, adicione labels aos nós:
```bash
docker node update --label-add zone=us-east-1 <node-id>
```

### Healthcheck Personalizado

O healthcheck já está configurado, mas você pode ajustar no `docker-stack.yml`:
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## 📊 Monitoramento

### Ver Uso de Recursos

```bash
docker stats $(docker ps -q --filter name=facecrop)
```

### Ver Eventos do Swarm

```bash
docker events --filter service=facecrop_facecrop-api
```

## 🔒 Segurança

1. **Use Docker Secrets** para API keys em produção
2. **Configure limites de recursos** no `docker-stack.yml`
3. **Use HTTPS** com um reverse proxy (nginx/traefik)
4. **Configure CORS** adequadamente no `main.py`
5. **Mantenha a imagem atualizada** com patches de segurança

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker service logs facecrop_facecrop-api --details

# Verificar se a imagem existe
docker images | grep facecrop-api
```

### Erro de conexão

```bash
# Verificar se o serviço está rodando
docker service ps facecrop_facecrop-api

# Verificar portas
docker service inspect facecrop_facecrop-api --pretty
```

### Problemas com OpenCV

Se houver problemas com OpenCV no container, verifique:
```bash
docker exec -it <container-id> python -c "import cv2; print(cv2.__version__)"
```

