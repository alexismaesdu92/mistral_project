# Variables
SHELL := /bin/bash
FRONT_DIR := front_end
BACK_DIR := back_end  # Ajustez selon votre structure de projet

# Couleurs pour les messages
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m  # No Color

.PHONY: all start stop clean install help

# Commande par défaut
all: help

# Démarrer l'application (backend et frontend)
start:
	@echo -e "${GREEN}Démarrage de l'application...${NC}"
	@echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter tous les services${NC}"
	@(trap 'kill 0' SIGINT; \
        (cd $(BACK_DIR) && python -m uvicorn app.main:app --reload --port 8000 2>&1 | tee backend.log) & \
        (cd $(FRONT_DIR) && npm start 2>&1 | tee frontend.log) & \
        wait)

# Installer les dépendances
install:
	@echo -e "${GREEN}Installation des dépendances du backend...${NC}"
	@cd $(BACK_DIR) && pip install -e .
	@echo -e "${GREEN}Installation des dépendances du frontend...${NC}"
	@cd $(FRONT_DIR) && npm install

# Nettoyer les fichiers générés
clean:
	@echo -e "${GREEN}Nettoyage des fichiers générés...${NC}"
	@cd $(FRONT_DIR) && npm run clean || true
	@rm -rf $(FRONT_DIR)/build || true
	@rm -rf $(FRONT_DIR)/node_modules/.cache || true
	@find . -name "__pycache__" -type d -exec rm -rf {} +

# Construire l'application pour la production
build:
	@echo -e "${GREEN}Construction du frontend pour la production...${NC}"
	@cd $(FRONT_DIR) && npm run build

# Afficher l'aide
help:
	@echo -e "${GREEN}Commandes disponibles:${NC}"
	@echo -e "  ${YELLOW}make install${NC}  - Installer toutes les dépendances"
	@echo -e "  ${YELLOW}make start${NC}    - Démarrer le backend et le frontend"
	@echo -e "  ${YELLOW}make build${NC}    - Construire l'application pour la production"
	@echo -e "  ${YELLOW}make clean${NC}    - Nettoyer les fichiers générés"
