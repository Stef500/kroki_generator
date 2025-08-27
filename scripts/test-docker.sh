#!/bin/bash
set -e

echo "🐳 Docker Integration Test Script"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    docker compose down -v --remove-orphans
    docker system prune -f
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Build and start services
echo "🏗️  Building and starting services..."
docker compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if ! docker compose ps | grep -q "Up"; then
    print_error "Services failed to start"
    docker compose logs
    exit 1
fi

print_status "Services started successfully"

# Run integration tests
echo "🧪 Running integration tests..."
if pytest tests/test_integration.py -v -m integration; then
    print_status "Integration tests passed"
else
    print_error "Integration tests failed"
    echo "📋 Service logs:"
    docker compose logs --tail=20
    exit 1
fi

# Test basic smoke scenarios
echo "💨 Running smoke tests..."

# Test homepage
if curl -f -s http://localhost:8080/ > /dev/null; then
    print_status "Homepage accessible"
else
    print_error "Homepage not accessible"
    exit 1
fi

# Test health endpoint
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
if echo "$HEALTH_RESPONSE" | jq -e '.service == "kroki-flask-generator"' > /dev/null; then
    print_status "Health endpoint working"
    HEALTH_STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.status')
    echo "   Health status: $HEALTH_STATUS"
    
    KROKI_STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.checks.kroki.status')
    echo "   Kroki status: $KROKI_STATUS"
else
    print_error "Health endpoint failed"
    exit 1
fi

# Test API endpoint (basic validation)
if curl -s -X POST http://localhost:8080/api/generate \
   -H "Content-Type: application/json" \
   -d '{}' | jq -e '.error' > /dev/null; then
    print_status "API validation working"
else
    print_error "API validation failed"
    exit 1
fi

print_status "All Docker integration tests passed!"
print_warning "Services will be cleaned up automatically"