#!/bin/bash

# ========================================
# Script de setup complet pour Mistral Chatbot
# ========================================
# 
# Ce script configure automatiquement l'environnement
# après un git clone

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_header() {
    echo -e "${PURPLE}========================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}========================================${NC}"
}

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

print_header "🚀 SETUP MISTRAL CHATBOT"

echo "Ce script va configurer votre environnement Mistral Chatbot"
echo "après un git clone."
echo ""

# Étape 1 : Vérifier les prérequis
print_step "Vérification des prérequis..."

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé."
    echo "📥 Veuillez installer Docker Desktop :"
    echo "   - macOS/Windows: https://www.docker.com/products/docker-desktop"
    echo "   - Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

# Vérifier Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé."
    echo "📥 Docker Compose est généralement inclus avec Docker Desktop."
    exit 1
fi

# Vérifier que Docker fonctionne
if ! docker info &> /dev/null; then
    print_error "Docker daemon n'est pas en cours d'exécution."
    echo "🔧 Veuillez démarrer Docker Desktop et réessayer."
    exit 1
fi

print_message "Prérequis vérifiés ✓"

# Étape 2 : Configuration de l'environnement
print_step "Configuration de l'environnement..."

# Créer le fichier .env s'il n'existe pas
if [ ! -f ".env" ]; then
    print_message "Création du fichier .env..."
    cp .env.example .env
    print_warning "⚠️  Fichier .env créé depuis .env.example"
else
    print_message "Fichier .env existe déjà ✓"
fi

# Vérifier la clé API
if grep -q "your_mistral_api_key_here" .env; then
    print_warning "⚠️  Clé API Mistral non configurée !"
    echo ""
    echo "🔑 Pour obtenir une clé API Mistral :"
    echo "   1. Allez sur https://console.mistral.ai"
    echo "   2. Créez un compte ou connectez-vous"
    echo "   3. Naviguez vers 'API Keys'"
    echo "   4. Créez une nouvelle clé API"
    echo "   5. Copiez la clé"
    echo ""
    
    read -p "Voulez-vous configurer votre clé API maintenant ? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Entrez votre clé API Mistral :"
        read -r api_key
        if [ ! -z "$api_key" ]; then
            # Remplacer la clé API dans le fichier .env
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/your_mistral_api_key_here/$api_key/" .env
            else
                # Linux
                sed -i "s/your_mistral_api_key_here/$api_key/" .env
            fi
            print_message "Clé API configurée ✓"
        else
            print_warning "Clé API vide, vous devrez la configurer manuellement"
        fi
    else
        print_warning "Vous devrez configurer la clé API manuellement dans .env"
    fi
else
    print_message "Clé API déjà configurée ✓"
fi

# Étape 3 : Créer les répertoires nécessaires
print_step "Création des répertoires..."
mkdir -p data/mistral_doc data/doc
print_message "Répertoires créés ✓"

# Étape 4 : Rendre les scripts exécutables
print_step "Configuration des permissions..."
chmod +x docker-start.sh docker-stop.sh test-docker-build.sh 2>/dev/null || true
print_message "Permissions configurées ✓"

# Étape 5 : Test de la configuration Docker
print_step "Test de la configuration Docker..."
if docker-compose config --quiet; then
    print_message "Configuration Docker valide ✓"
else
    print_error "Configuration Docker invalide"
    exit 1
fi

# Étape 6 : Proposer de démarrer l'application
echo ""
print_header "🎉 SETUP TERMINÉ"
echo ""
print_message "Votre environnement Mistral Chatbot est prêt !"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. Vérifiez votre clé API dans .env"
echo "   2. Démarrez l'application avec : ./docker-start.sh"
echo "   3. Accédez à l'interface : http://localhost:3000"
echo ""

read -p "Voulez-vous démarrer l'application maintenant ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Démarrage de l'application..."
    ./docker-start.sh
else
    echo ""
    echo "🚀 Pour démarrer l'application plus tard :"
    echo "   ./docker-start.sh"
    echo ""
    echo "📚 Documentation disponible :"
    echo "   - README.md"
    echo "   - QUICK_START.md"
    echo "   - DOCKER_README.md"
fi
