#!/bin/bash
# Kroki Flask Generator - Installation Script
# Installs and runs the complete Kroki diagram generation service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://raw.githubusercontent.com/Stef500/kroki_generator/main"
COMPOSE_FILE="deploy/docker-compose.yml"
DEFAULT_PORT=8080
APP_PORT=${APP_PORT:-$DEFAULT_PORT}

echo -e "${BLUE}🚀 Kroki Flask Generator - Installation${NC}"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé.${NC}"
    echo "   Installez Docker depuis: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose n'est pas disponible.${NC}"
    echo "   Installez Docker Compose depuis: https://docs.docker.com/compose/install/"
    exit 1
fi

# Set docker-compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo -e "${BLUE}📦 Récupération de la configuration de déploiement...${NC}"

# Download docker-compose.yml from GitHub
if curl -sSL "${REPO_URL}/${COMPOSE_FILE}" -o docker-compose.yml; then
    echo -e "${GREEN}✅ Configuration récupérée avec succès${NC}"
else
    echo -e "${RED}❌ Impossible de récupérer la configuration${NC}"
    echo "   Vérifiez votre connexion internet ou récupérez manuellement :"
    echo "   ${REPO_URL}/${COMPOSE_FILE}"
    exit 1
fi

echo -e "${BLUE}📦 Téléchargement des images Docker...${NC}"

# Pull latest images
if $COMPOSE_CMD pull; then
    echo -e "${GREEN}✅ Images téléchargées avec succès${NC}"
else
    echo -e "${YELLOW}⚠️  Erreur lors du téléchargement des images${NC}"
    echo "   Continuons quand même..."
fi

# Check if port is already in use
if lsof -i :$APP_PORT > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Le port $APP_PORT est déjà utilisé${NC}"
    echo "   Définissez un autre port avec: APP_PORT=3000 ./install.sh"
    echo "   Ou arrêtez le service utilisant le port $APP_PORT"
    read -p "Continuer quand même ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}🎯 Démarrage des services...${NC}"

# Start services
export APP_PORT
if $COMPOSE_CMD up -d; then
    echo -e "${GREEN}✅ Services démarrés avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors du démarrage des services${NC}"
    echo "   Consultez les logs avec: $COMPOSE_CMD logs"
    exit 1
fi

echo -e "${BLUE}⏳ Vérification du démarrage de l'application...${NC}"

# Wait for services to be ready
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:$APP_PORT/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application démarrée et accessible !${NC}"
        echo
        echo "🌐 Application disponible sur: http://localhost:$APP_PORT"
        echo "🔗 Interface web: http://localhost:$APP_PORT"
        echo "📊 Health check: http://localhost:$APP_PORT/health"
        echo
        echo -e "${BLUE}📋 Commandes utiles:${NC}"
        echo "   Voir les logs:     $COMPOSE_CMD logs -f"
        echo "   Arrêter:          $COMPOSE_CMD down"
        echo "   Redémarrer:       $COMPOSE_CMD restart"
        echo "   Mettre à jour:    $COMPOSE_CMD pull && $COMPOSE_CMD up -d"
        echo
        exit 0
    fi
    
    echo -e "${YELLOW}.${NC}" | tr -d '\n'
    sleep 2
    attempt=$((attempt + 1))
done

echo
echo -e "${YELLOW}⚠️  L'application met plus de temps que prévu à démarrer${NC}"
echo "   Vérifiez les logs avec: $COMPOSE_CMD logs"
echo "   L'application sera bientôt disponible sur: http://localhost:$APP_PORT"