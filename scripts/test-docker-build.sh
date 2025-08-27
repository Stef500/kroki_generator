#!/bin/bash

# Script pour tester la construction Docker localement
# Usage: ./scripts/test-docker-build.sh [username]

set -e

USERNAME=${1:-"your-dockerhub-username"}
IMAGE_NAME="kroki-flask-generator"
TAG="test-$(date +%Y%m%d-%H%M%S)"

echo "🔨 Building Docker image locally..."
echo "Image: ${USERNAME}/${IMAGE_NAME}:${TAG}"

# Build de l'image
docker build -t "${USERNAME}/${IMAGE_NAME}:${TAG}" .

echo "✅ Image built successfully!"

# Test de l'image
echo "🧪 Testing image..."
docker run --rm -d -p 8080:8080 --name "test-${IMAGE_NAME}" "${USERNAME}/${IMAGE_NAME}:${TAG}"

# Attendre que le service démarre
echo "⏳ Waiting for service to start..."
sleep 10

# Test health check
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
    docker logs "test-${IMAGE_NAME}"
    exit 1
fi

# Test page d'accueil
if curl -f http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ Homepage accessible!"
else
    echo "❌ Homepage not accessible!"
    docker logs "test-${IMAGE_NAME}"
    exit 1
fi

# Nettoyage
docker stop "test-${IMAGE_NAME}"

echo "🎉 All tests passed!"
echo "💡 To push to DockerHub (after configuring credentials):"
echo "   docker tag ${USERNAME}/${IMAGE_NAME}:${TAG} ${USERNAME}/${IMAGE_NAME}:latest"
echo "   docker push ${USERNAME}/${IMAGE_NAME}:latest"

# Afficher la taille de l'image
echo "📊 Image size:"
docker images "${USERNAME}/${IMAGE_NAME}:${TAG}" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"