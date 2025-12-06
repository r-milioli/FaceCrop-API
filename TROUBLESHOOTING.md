# Guia de Troubleshooting - FaceCrop API

## Problemas Comuns e Soluções

### 1. Erro ao iniciar o servidor

**Sintoma:** Erro ao executar `python main.py`

**Soluções:**
```bash
# Verificar se todas as dependências estão instaladas
pip install -r requirements.txt

# Verificar se há erros de sintaxe
python -m py_compile main.py

# Tentar importar o módulo
python -c "import main; print('OK')"
```

### 2. Erro de porta já em uso

**Sintoma:** `Address already in use` ou `Port 8000 is already in use`

**Soluções:**
```bash
# Windows - Verificar qual processo está usando a porta
netstat -ano | findstr :8000

# Matar o processo (substitua PID pelo número encontrado)
taskkill /PID <PID> /F

# Ou usar outra porta
python main.py
# E no código, alterar: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 3. Erro de importação

**Sintoma:** `ModuleNotFoundError` ou `ImportError`

**Soluções:**
```bash
# Verificar se está no diretório correto
cd "C:\Users\Robson\Documents\API de Detecção Facial"

# Verificar estrutura de diretórios
dir utils

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### 4. Erro com OpenCV

**Sintoma:** `ImportError: libGL.so.1` ou similar

**Solução:**
- Certifique-se de estar usando `opencv-python-headless` no `requirements.txt`
- Reinstale: `pip install opencv-python-headless --force-reinstall`

### 5. API não responde

**Sintoma:** Timeout ou conexão recusada

**Soluções:**
```bash
# Verificar se o servidor está rodando
python test_local.py

# Verificar logs do servidor
# Execute python main.py e veja as mensagens no console

# Verificar firewall
# Certifique-se de que a porta 8000 não está bloqueada
```

### 6. Erro 401 Unauthorized

**Sintoma:** Todas as requisições retornam 401

**Soluções:**
```bash
# Verificar se o arquivo .env existe
dir .env

# Criar arquivo .env se não existir
copy env.example .env

# Editar .env e definir API_KEY
# API_KEY=sua-chave-secreta-aqui

# Verificar se a API key está sendo lida
python -c "from utils.auth import VALID_API_KEY; print('API Key:', VALID_API_KEY[:10] + '...')"
```

### 7. Erro ao processar imagens

**Sintoma:** Erro 500 ao fazer upload de imagem

**Soluções:**
```bash
# Verificar se OpenCV está funcionando
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

# Verificar se Pillow está instalado
python -c "from PIL import Image; print('Pillow OK')"

# Verificar logs detalhados no servidor
```

### 8. Middleware bloqueando paths válidos

**Sintoma:** `/docs` ou outros endpoints retornam 404

**Solução:**
- O middleware foi atualizado para permitir paths válidos da API
- Se ainda houver problemas, verifique `utils/security.py`

## Testes Rápidos

### Teste 1: Verificar instalação
```bash
python -c "import fastapi, uvicorn, cv2, PIL; print('✅ Todas as dependências OK')"
```

### Teste 2: Verificar servidor
```bash
python test_local.py
```

### Teste 3: Testar manualmente
```bash
# Terminal 1: Iniciar servidor
python main.py

# Terminal 2: Testar
curl http://localhost:8000/health
```

## Comandos Úteis

```bash
# Verificar versão do Python
python --version

# Verificar dependências instaladas
pip list | findstr -i "fastapi uvicorn opencv pillow"

# Limpar cache do Python
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"

# Reinstalar tudo do zero
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

## Logs e Debug

Para ver logs detalhados, execute:
```bash
python main.py
```

Ou com uvicorn diretamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

## Ainda com problemas?

1. Verifique os logs do servidor
2. Execute `python test_local.py` para diagnóstico
3. Verifique se todas as dependências estão instaladas
4. Certifique-se de estar usando Python 3.9+

