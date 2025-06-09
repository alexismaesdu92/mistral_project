# ========================================
# Makefile pour Mistral Chatbot
# ========================================

# Variables
SHELL := /bin/bash
FRONT_DIR := front_end
BACK_DIR := back_end

# Couleurs pour les messages
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m  # No Color

.PHONY: all help install clean build dev-start docker-up docker-down docker-build docker-logs docker-restart docker-clean docker-status

# Commande par défaut
all: help

# ========================================
# COMMANDES DOCKER (RECOMMANDÉES)
# ========================================

# Démarrer l'application avec Docker
docker-up:
	@echo -e "${GREEN}🐳 Démarrage de l'application avec Docker...${NC}"
	@./docker-start.sh

# Arrêter l'application Docker
docker-down:
	@echo -e "${GREEN}🛑 Arrêt de l'application Docker...${NC}"
	@./docker-stop.sh

# Construire les images Docker
docker-build:
	@echo -e "${GREEN}🔨 Construction des images Docker...${NC}"
	@docker-compose build

# Voir les logs Docker
docker-logs:
	@echo -e "${GREEN}📊 Affichage des logs Docker...${NC}"
	@docker-compose logs -f

# Redémarrer l'application Docker
docker-restart:
	@echo -e "${GREEN}🔄 Redémarrage de l'application Docker...${NC}"
	@docker-compose restart

# Nettoyer Docker complètement
docker-clean:
	@echo -e "${YELLOW}🧹 Nettoyage Docker complet...${NC}"
	@docker-compose down --rmi all --volumes
	@docker system prune -f

# Voir l'état des services Docker
docker-status:
	@echo -e "${GREEN}📋 État des services Docker...${NC}"
	@docker-compose ps

# ========================================
# COMMANDES DE DÉVELOPPEMENT LOCAL
# ========================================

# Installer les dépendances
install:
	@echo -e "${GREEN}📦 Installation des dépendances...${NC}"
	@echo -e "${BLUE}Backend...${NC}"
	@cd $(BACK_DIR) && pip install -e .
	@echo -e "${BLUE}Frontend...${NC}"
	@cd $(FRONT_DIR) && npm install
	@echo -e "${GREEN}✅ Installation terminée${NC}"

# Démarrer en mode développement (sans Docker)
dev-start:
	@echo -e "${GREEN}💻 Démarrage en mode développement...${NC}"
	@echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter tous les services${NC}"
	@(trap 'kill 0' SIGINT; \
        (cd $(BACK_DIR) && python -m uvicorn app.main:app --reload --port 8000 2>&1 | tee backend.log) & \
        (cd $(FRONT_DIR) && npm start 2>&1 | tee frontend.log) & \
        wait)

# Construire l'application pour la production
build:
	@echo -e "${GREEN}🏗️  Construction pour la production...${NC}"
	@cd $(FRONT_DIR) && npm run build
	@echo -e "${GREEN}✅ Build terminé${NC}"

# Nettoyer les fichiers générés
clean:
	@echo -e "${GREEN}🧹 Nettoyage des fichiers générés...${NC}"
	@cd $(FRONT_DIR) && npm run clean || true
	@rm -rf $(FRONT_DIR)/build || true
	@rm -rf $(FRONT_DIR)/node_modules/.cache || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -f *.log
	@echo -e "${GREEN}✅ Nettoyage terminé${NC}"

# ========================================
# AIDE ET INFORMATIONS
# ========================================

# Afficher l'aide
help:
	@echo -e "${GREEN}========================================${NC}"
	@echo -e "${GREEN}🚀 Mistral Chatbot - Commandes disponibles${NC}"
	@echo -e "${GREEN}========================================${NC}"
	@echo ""
	@echo -e "${YELLOW}🐳 Commandes Docker (recommandées):${NC}"
	@echo -e "  ${BLUE}make docker-up${NC}      - Démarrer avec Docker"
	@echo -e "  ${BLUE}make docker-down${NC}    - Arrêter Docker"
	@echo -e "  ${BLUE}make docker-build${NC}   - Construire les images"
	@echo -e "  ${BLUE}make docker-logs${NC}    - Voir les logs"
	@echo -e "  ${BLUE}make docker-restart${NC} - Redémarrer"
	@echo -e "  ${BLUE}make docker-status${NC}  - État des services"
	@echo -e "  ${BLUE}make docker-clean${NC}   - Nettoyer complètement"
	@echo ""
	@echo -e "${YELLOW}💻 Développement local:${NC}"
	@echo -e "  ${BLUE}make install${NC}        - Installer les dépendances"
	@echo -e "  ${BLUE}make dev-start${NC}      - Démarrer en mode dev"
	@echo -e "  ${BLUE}make build${NC}          - Build de production"
	@echo -e "  ${BLUE}make clean${NC}          - Nettoyer les fichiers"
	@echo ""
	@echo -e "${YELLOW}🌐 Accès à l'application:${NC}"
	@echo -e "  Frontend:    ${BLUE}http://localhost:3000${NC}"
	@echo -e "  Backend:     ${BLUE}http://localhost:8000${NC}"
	@echo -e "  API Docs:    ${BLUE}http://localhost:8000/docs${NC}"
	@echo ""
	@echo -e "${YELLOW}📚 Documentation:${NC}"
	@echo -e "  Docker:      ${BLUE}cat DOCKER_README.md${NC}"
	@echo -e "  Déploiement: ${BLUE}cat DEPLOYMENT.md${NC}"

# Alias pour la compatibilité
start: dev-start
