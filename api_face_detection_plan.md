# Plano de Ação - API de Detecção Facial para Corte de Vídeo

## 1. Objetivo

Criar uma API leve que detecta a posição do nariz do falante em um frame de vídeo para realizar corte inteligente 9:16.

---

## 2. Especificações Técnicas

### 2.1 Linguagem e Framework

**Python com FastAPI**

- Mais leve que Flask para APIs
- Async nativo (melhor performance)
- Documentação automática (Swagger)
- Melhor integração com MediaPipe

### 2.2 Biblioteca de Detecção

**MediaPipe Face Mesh**

- 468 pontos faciais
- Processamento local
- Gratuito e open-source

---

## 3. Requisitos Funcionais

### 3.1 Input (Múltiplo)

- **Opção 1:** Upload de arquivo (POST multipart/form-data)
- **Opção 2:** URL da imagem (POST JSON com URL)
- Formatos aceitos: JPG, PNG, WEBP

### 3.2 Processamento

1. Recebe a imagem
2. Detecta todas as faces
3. **Se múltiplas faces:** seleciona a maior (área do bounding box)
4. **Se nenhuma face:** retorna centro da imagem
5. Localiza ponto do nariz (tip of nose - landmark #1)
6. Converte coordenadas para pixels absolutos

### 3.3 Output (JSON)

```json
{
  "x": 960,
  "y": 540,
  "face_detected": true,
  "image_width": 1920,
  "image_height": 1080,
  "confidence": 0.95
}
```

**Campos:**

- `x`: coordenada horizontal do nariz (pixels)
- `y`: coordenada vertical do nariz (pixels)
- `face_detected`: boolean (true/false)
- `image_width`: largura da imagem original
- `image_height`: altura da imagem original
- `confidence`: nível de confiança da detecção (0-1)

---

## 4. Estrutura da API

### 4.1 Endpoints

**POST /detect**

- Recebe upload de imagem
- Retorna coordenadas

**POST /detect-url**

- Recebe URL da imagem
- Baixa e processa
- Retorna coordenadas

**GET /health**

- Verifica status da API
- Retorna `{"status": "ok"}`

---

## 5. Fluxo de Processamento

```
1. Receber imagem (upload ou URL)
   ↓
2. Validar formato e tamanho
   ↓
3. Converter para RGB (MediaPipe requer)
   ↓
4. Processar com MediaPipe Face Mesh
   ↓
5. Detectar faces
   ↓
6. [Se múltiplas] → Calcular área de cada face → Selecionar maior
   ↓
7. [Se nenhuma] → Retornar centro da imagem (width/2, height/2)
   ↓
8. Extrair landmark do nariz (#1)
   ↓
9. Converter coordenadas normalizadas para pixels
   ↓
10. Retornar JSON com coordenadas
```

---

## 6. Requisitos Não-Funcionais

### 6.1 Performance

- Tempo de resposta: < 500ms por imagem
- Suporte a imagens até 4K
- Processamento assíncrono

### 6.2 Segurança

- Validação de formato de arquivo
- Limite de tamanho de upload (ex: 10MB)
- Timeout para download de URLs (5s)
- Sanitização de URLs

### 6.3 Tratamento de Erros

- Formato de arquivo inválido
- Imagem corrompida
- URL inacessível
- Timeout de processamento

---

## 7. Dependências

```
- Python 3.9+
- FastAPI
- Uvicorn (servidor ASGI)
- MediaPipe
- OpenCV (cv2)
- Pillow (PIL)
- requests (para download de URLs)
- python-multipart (para upload)
```

---

## 8. Estrutura do Projeto

```
api-face-detection/
├── main.py              # Aplicação FastAPI
├── requirements.txt     # Dependências
├── Dockerfile          # Container (opcional)
├── .env                # Configurações
└── utils/
    ├── detector.py     # Lógica MediaPipe
    └── image_handler.py # Download/Upload
```

---

## 9. Integração com n8n

### 9.1 Via Upload

```
n8n → FFmpeg extrai frame → HTTP Request (POST /detect) → Recebe coordenadas
```

### 9.2 Via URL

```
n8n → FFmpeg extrai frame → Upload para storage → HTTP Request (POST /detect-url) → Recebe coordenadas
```

---

## 10. Casos de Uso Cobertos

✅ **Caso 1:** 1 pessoa falando (podcast solo)

- Detecta face única
- Retorna posição do nariz

✅ **Caso 2:** 2+ pessoas no frame

- Detecta múltiplas faces
- Seleciona a maior (presumivelmente mais próxima/central)
- Retorna posição do nariz da face selecionada

✅ **Caso 3:** Nenhuma face detectada (erro/frame sem pessoa)

- Retorna centro da imagem como fallback
- Flag `face_detected: false`

✅ **Caso 4:** Imagem em URL ou arquivo local

- Suporta ambos métodos de input

---

## 11. Próximos Passos para Implementação

1. ✅ Definir requisitos (completo)
2. ⏭️ Criar estrutura do projeto
3. ⏭️ Implementar detector com MediaPipe
4. ⏭️ Implementar endpoints FastAPI
5. ⏭️ Testar com imagens de exemplo
6. ⏭️ Containerizar com Docker (opcional)
7. ⏭️ Deploy e integração com n8n

---

## 12. Observações Finais

Este documento serve como guia completo para o desenvolvimento da API de detecção facial. A arquitetura proposta é escalável, eficiente e atende todos os requisitos do projeto de corte inteligente de vídeos para formato vertical (9:16).

A escolha do MediaPipe garante precisão e performance sem custos adicionais, enquanto o FastAPI proporciona uma base sólida para uma API moderna e bem documentada.