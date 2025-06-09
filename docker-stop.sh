#!/bin/bash

# ========================================
# Script d'arrêt pour Mistral Chatbot
# ========================================

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo "🛑 Arrêt de l'application Mistral Chatbot"
echo "=========================================="

# Arrêter et supprimer les conteneurs
print_step "Arrêt des conteneurs..."
docker-compose down

print_message "Application arrêtée avec succès ✓"
echo ""
echo "📋 Commandes utiles :"
echo "   Redémarrer:                    ./docker-start.sh"
echo "   Supprimer les images:          docker-compose down --rmi all"
echo "   Supprimer tout (+ volumes):    docker-compose down --rmi all --volumes"
echo "   Nettoyer Docker:               docker system prune -a"
echo ""

# Options avancées
read -p "Voulez-vous également supprimer les images Docker ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Suppression des images..."
    docker-compose down --rmi all
    print_message "Images supprimées ✓"
fi

read -p "Voulez-vous supprimer les volumes (ATTENTION: supprime les données) ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Suppression des volumes..."
    docker-compose down --volumes
    print_message "Volumes supprimés ✓"
fi
