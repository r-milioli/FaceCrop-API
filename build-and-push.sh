#!/bin/bash

# Script para build e push da imagem Docker para Docker Hub
# Uso: ./build-and-push.sh [tag]

set -e

IMAGE_NAME="automacaodebaixocusto/facecrop-api"
TAG=${1:-latest}

echo "🔨 Building Docker image: ${IMAGE_NAME}:${TAG}"

# Build da imagem
docker build -t ${IMAGE_NAME}:${TAG} .

echo "✅ Build concluído!"

# Perguntar se deseja fazer push
read -p "Deseja fazer push para Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📤 Fazendo push para Docker Hub..."
    docker push ${IMAGE_NAME}:${TAG}
    echo "✅ Push concluído!"
else
    echo "⏭️  Push cancelado."
fi

