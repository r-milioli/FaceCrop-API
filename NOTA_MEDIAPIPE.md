# Nota sobre MediaPipe

## Problema Encontrado

O MediaPipe não está disponível para Python 3.13 ainda. Por isso, a implementação foi adaptada para usar **OpenCV** com detecção de faces via Haar Cascade.

## Solução Implementada

A API agora usa:
- **OpenCV** com Haar Cascade para detecção de faces
- Estimação da posição do nariz baseada na geometria da face detectada
- Compatível com Python 3.13+

## Migração Futura para MediaPipe

Quando o MediaPipe estiver disponível para Python 3.13, você pode:

1. Instalar MediaPipe:
```bash
pip install mediapipe
```

2. Substituir o conteúdo de `utils/detector.py` pela versão original que usa MediaPipe Face Mesh (mais precisa, com 468 landmarks).

## Alternativa: Usar Python 3.11 ou 3.12

Se você precisar usar MediaPipe agora, pode criar um ambiente virtual com Python 3.11 ou 3.12:

```bash
# Instalar Python 3.11 ou 3.12
# Criar ambiente virtual
python3.11 -m venv venv
# ou
python3.12 -m venv venv

# Ativar e instalar
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Depois, atualize o `requirements.txt` para incluir:
```
mediapipe>=0.10.0
```

E restaure o código original do `utils/detector.py` que usa MediaPipe.

