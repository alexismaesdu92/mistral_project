#!/bin/bash

# ========================================
# Script de démarrage pour Mistral Chatbot
# ========================================
# 
# Ce script vérifie les prérequis et démarre l'application
# avec Docker Compose

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo "🚀 Démarrage de l'application Mistral Chatbot avec Docker"
echo "========================================================"

# Vérifier que Docker est installé
print_step "Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé."
    echo "📥 Veuillez télécharger et installer Docker Desktop depuis :"
    echo "   https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé."
    echo "📥 Docker Compose est généralement inclus avec Docker Desktop."
    exit 1
fi

print_message "Docker et Docker Compose sont installés ✓"

# Vérifier que Docker fonctionne
print_step "Vérification du daemon Docker..."
if ! docker info &> /dev/null; then
    print_error "Docker daemon n'est pas en cours d'exécution."
    echo "🔧 Veuillez démarrer Docker Desktop et réessayer."
    exit 1
fi

print_message "Docker daemon fonctionne ✓"

# Vérifier la présence du fichier .env
print_step "Vérification de la configuration..."
if [ ! -f ".env" ]; then
    print_warning "Fichier .env non trouvé."
    echo "📋 Création du fichier .env depuis .env.example..."
    cp .env.example .env
    print_warning "⚠️  IMPORTANT: Éditez le fichier .env et ajoutez votre clé API Mistral !"
    echo "   1. Ouvrez le fichier .env"
    echo "   2. Remplacez 'your_mistral_api_key_here' par votre vraie clé API"
    echo "   3. Obtenez une clé sur : https://console.mistral.ai"
    echo ""
    read -p "Appuyez sur Entrée quand vous avez configuré votre clé API..."
fi

# Vérifier que la clé API est configurée
if grep -q "your_mistral_api_key_here" .env; then
    print_error "La clé API Mistral n'est pas configurée dans le fichier .env"
    echo "🔑 Veuillez éditer le fichier .env et remplacer 'your_mistral_api_key_here'"
    echo "   par votre vraie clé API Mistral."
    exit 1
fi

print_message "Configuration vérifiée ✓"

# Créer les répertoires nécessaires
print_step "Création des répertoires nécessaires..."
mkdir -p data/mistral_doc data/doc

# Arrêter les conteneurs existants s'ils tournent
print_step "Arrêt des conteneurs existants..."
docker-compose down --remove-orphans 2>/dev/null || true

# Construire et démarrer les services
print_step "Construction et démarrage des services..."
echo "⏳ Cela peut prendre quelques minutes lors du premier démarrage..."
docker-compose up --build -d

# Attendre que les services soient prêts
print_step "Attente du démarrage des services..."
echo "⏳ Vérification de la santé des services..."

# Attendre le backend
for i in {1..30}; do
    if curl -f http://localhost:8000/ &>/dev/null; then
        print_message "Backend prêt ✓"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Le backend n'a pas démarré dans les temps"
        docker-compose logs backend
        exit 1
    fi
    sleep 2
done

# Attendre le frontend
for i in {1..30}; do
    if curl -f http://localhost:3000/health &>/dev/null; then
        print_message "Frontend prêt ✓"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Le frontend n'a pas démarré dans les temps"
        docker-compose logs frontend
        exit 1
    fi
    sleep 2
done

# Vérifier l'état des services
print_step "Vérification de l'état des services..."
docker-compose ps

echo ""
echo "🎉 Application démarrée avec succès !"
echo "========================================"
echo ""
echo "🌐 Accès à l'application :"
echo "   Frontend:     http://localhost:3000"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo ""
echo "📋 Commandes utiles :"
echo "   Voir les logs:        docker-compose logs -f"
echo "   Arrêter:             ./docker-stop.sh"
echo "   Redémarrer:          docker-compose restart"
echo ""

# Demander si l'utilisateur veut voir les logs
read -p "Voulez-vous voir les logs en temps réel ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Affichage des logs (Ctrl+C pour quitter)..."
    docker-compose logs -f
fi
