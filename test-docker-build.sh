#!/bin/bash

# Script de test pour le build Docker

set -e

echo "🧪 Test du build Docker pour Mistral Chatbot"
echo "=============================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "${YELLOW}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test 1: Build du backend seulement
print_step "Test du build backend..."
if docker build -f Dockerfile.backend -t test-backend .; then
    print_success "Build backend réussi ✓"
else
    print_error "Échec du build backend ✗"
    exit 1
fi

# Test 2: Build du frontend seulement
print_step "Test du build frontend..."
if docker build -f Dockerfile.frontend -t test-frontend .; then
    print_success "Build frontend réussi ✓"
else
    print_error "Échec du build frontend ✗"
    exit 1
fi

# Test 3: Validation de la configuration docker-compose
print_step "Validation de docker-compose..."
if docker-compose config --quiet; then
    print_success "Configuration docker-compose valide ✓"
else
    print_error "Configuration docker-compose invalide ✗"
    exit 1
fi

# Nettoyage des images de test
print_step "Nettoyage des images de test..."
docker rmi test-backend test-frontend 2>/dev/null || true

print_success "Tous les tests sont passés ! 🎉"
echo ""
echo "Vous pouvez maintenant démarrer l'application avec :"
echo "  ./docker-start.sh"
