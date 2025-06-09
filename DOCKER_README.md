# 🐳 Guide Docker - Mistral Chatbot

Ce guide vous explique comment déployer l'application Mistral Chatbot avec Docker.

## 📋 Prérequis

### Logiciels requis
- [Docker Desktop](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (inclus avec Docker Desktop)

### Ressources système
- **RAM** : Minimum 4GB, recommandé 8GB
- **Stockage** : Minimum 10GB d'espace libre
- **Ports** : 3000 et 8000 doivent être libres

### Clé API Mistral
- Compte sur [Mistral AI Console](https://console.mistral.ai)
- Clé API valide (obligatoire)

## 🚀 Démarrage rapide

### 1. Configuration initiale

```bash
# Cloner le projet (si pas déjà fait)
git clone <votre-repo>
cd mistral_project

# Copier le fichier d'environnement
cp .env.example .env

# Éditer le fichier .env et ajouter votre clé API Mistral
nano .env
```

**Important** : Remplacez `your_mistral_api_key_here` par votre vraie clé API dans le fichier `.env`.

### 2. Démarrage automatique

```bash
# Script de démarrage automatique (recommandé)
./docker-start.sh
```

### 3. Démarrage manuel

```bash
# Construire et démarrer les services
docker-compose up --build -d

# Voir les logs
docker-compose logs -f
```

## 🌐 Accès à l'application

Une fois démarrée, l'application sera disponible sur :

- **Interface utilisateur** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Health check** : http://localhost:3000/health

## 🛠️ Gestion de l'application

### Commandes de base

```bash
# Démarrer l'application
./docker-start.sh

# Arrêter l'application
./docker-stop.sh

# Voir les logs en temps réel
docker-compose logs -f

# Voir l'état des services
docker-compose ps

# Redémarrer un service
docker-compose restart backend
docker-compose restart frontend
```

### Commandes avancées

```bash
# Reconstruire les images
docker-compose build --no-cache

# Redémarrer complètement
docker-compose down && docker-compose up --build -d

# Accéder au shell d'un conteneur
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🔧 Configuration

### Variables d'environnement

Le fichier `.env` contient toutes les configurations :

```env
# API Mistral (OBLIGATOIRE)
MISTRAL_API_KEY=votre_clé_api_ici

# Ports (optionnel)
FRONTEND_PORT=3000
BACKEND_PORT=8000

# Modèle Mistral (optionnel)
MISTRAL_MODEL=mistral-medium

# Niveau de logs (optionnel)
LOG_LEVEL=INFO
```

### Personnalisation des ports

Pour changer les ports, modifiez le fichier `.env` :

```env
FRONTEND_PORT=8080
BACKEND_PORT=9000
```

Puis redémarrez l'application.

## 📁 Architecture Docker

### Services

1. **Backend** (`mistral-backend`)
   - Image : Python 3.11 slim
   - Framework : FastAPI
   - Port : 8000
   - Volumes : `./data`, `backend_logs`

2. **Frontend** (`mistral-frontend`)
   - Image : nginx alpine
   - Framework : React (build de production)
   - Port : 3000
   - Build multi-stage optimisé

### Volumes persistants

- `./data` : Données vectorielles et documents
- `backend_logs` : Logs du backend

### Réseau

- Réseau bridge `mistral-network`
- Communication interne entre services

## 🐛 Dépannage

### Problèmes courants

#### 1. Docker daemon non démarré
```bash
# Erreur : Cannot connect to the Docker daemon
# Solution : Démarrer Docker Desktop
open -a Docker  # macOS
# Ou démarrer Docker Desktop manuellement
```

#### 2. Ports déjà utilisés
```bash
# Vérifier les ports
lsof -i :3000
lsof -i :8000

# Solution : Modifier les ports dans .env ou arrêter les autres services
```

#### 3. Clé API manquante
```bash
# Erreur : MISTRAL_API_KEY environment variable not set
# Solution : Configurer la clé API dans .env
```

#### 4. Problème de build
```bash
# Nettoyer et reconstruire
docker-compose down --rmi all
docker-compose build --no-cache
docker-compose up -d
```

### Logs de débogage

```bash
# Logs détaillés
docker-compose logs --tail=100 backend
docker-compose logs --tail=100 frontend

# Logs en temps réel
docker-compose logs -f

# Informations système
docker system df
docker system info
```

## 🔄 Mise à jour

### Mise à jour simple
```bash
# Arrêter l'application
./docker-stop.sh

# Récupérer les mises à jour (si depuis Git)
git pull

# Redémarrer
./docker-start.sh
```

### Mise à jour complète
```bash
# Arrêter et nettoyer
docker-compose down --rmi all

# Reconstruire
docker-compose build --no-cache

# Redémarrer
docker-compose up -d
```

## 🛡️ Sécurité

### Bonnes pratiques

1. **Variables d'environnement**
   - Ne jamais commiter le fichier `.env`
   - Utiliser des secrets en production

2. **Réseau**
   - Configurer un reverse proxy en production
   - Activer HTTPS
   - Limiter les CORS origins

3. **Images**
   - Utiliser des utilisateurs non-root
   - Mettre à jour régulièrement les images de base

## 📊 Monitoring

### Health checks

Les services incluent des health checks automatiques :

```bash
# Vérifier la santé des services
docker-compose ps

# Tester manuellement
curl http://localhost:8000/        # Backend
curl http://localhost:3000/health  # Frontend
```

### Métriques

```bash
# Utilisation des ressources
docker stats

# Espace disque
docker system df

# Informations détaillées
docker inspect mistral-backend
docker inspect mistral-frontend
```

## 🧹 Nettoyage

### Nettoyage standard
```bash
# Arrêter et supprimer les conteneurs
./docker-stop.sh
```

### Nettoyage complet
```bash
# Supprimer tout (conteneurs, images, volumes)
docker-compose down --rmi all --volumes

# Nettoyer le système Docker
docker system prune -a
```

## 📞 Support

### Informations utiles pour le support

```bash
# Versions
docker --version
docker-compose --version

# Configuration
docker-compose config

# Logs complets
docker-compose logs > logs.txt
```

### Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Mistral AI Console](https://console.mistral.ai)

---

**Note** : Cette configuration Docker est optimisée pour le développement et les tests. Pour la production, des ajustements supplémentaires sont recommandés (HTTPS, secrets, monitoring, etc.).
