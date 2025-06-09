# 🚀 Guide de Setup Post-Clone

Ce guide vous accompagne étape par étape après avoir cloné le projet Mistral Chatbot.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé et en cours d'exécution
- Un compte [Mistral AI](https://console.mistral.ai) avec une clé API

## ⚡ Setup automatique (Recommandé)

### Option 1 : Script de setup complet

```bash
# Après le git clone
cd mistral_project

# Lancer le setup automatique
./setup.sh
```

Le script va :
- ✅ Vérifier les prérequis (Docker, Docker Compose)
- ✅ Créer le fichier `.env` depuis `.env.example`
- ✅ Vous demander votre clé API Mistral
- ✅ Créer les répertoires nécessaires
- ✅ Configurer les permissions
- ✅ Proposer de démarrer l'application

### Option 2 : Validation puis setup

```bash
# Valider l'installation
./validate-setup.sh

# Si tout est OK, lancer le setup
./setup.sh
```

## 🔧 Setup manuel

Si vous préférez configurer manuellement :

### 1. Validation de l'environnement

```bash
# Vérifier que tous les fichiers sont présents
./validate-setup.sh
```

### 2. Configuration de l'environnement

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer le fichier .env
nano .env  # ou votre éditeur préféré
```

**Important** : Remplacez `your_mistral_api_key_here` par votre vraie clé API.

### 3. Obtenir une clé API Mistral

1. Allez sur https://console.mistral.ai
2. Créez un compte ou connectez-vous
3. Naviguez vers "API Keys"
4. Créez une nouvelle clé API
5. Copiez la clé dans votre fichier `.env`

### 4. Créer les répertoires

```bash
mkdir -p data/mistral_doc data/doc
```

### 5. Configurer les permissions

```bash
chmod +x *.sh
```

### 6. Démarrer l'application

```bash
./docker-start.sh
```

## 🌐 Accès à l'application

Une fois démarrée :

- **Interface** : http://localhost:3000
- **API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🛠️ Commandes utiles

```bash
# Voir l'aide complète
make help

# Démarrer l'application
make docker-up

# Voir les logs
make docker-logs

# Arrêter l'application
make docker-down

# Redémarrer
make docker-restart

# Nettoyer complètement
make docker-clean
```

## 🐛 Dépannage

### Docker daemon non démarré

```bash
# macOS
open -a Docker

# Vérifier que Docker fonctionne
docker info
```

### Ports déjà utilisés

```bash
# Vérifier les ports
lsof -i :3000
lsof -i :8000

# Arrêter les processus si nécessaire
sudo kill -9 $(lsof -t -i:3000)
sudo kill -9 $(lsof -t -i:8000)
```

### Problème de build Docker

```bash
# Nettoyer et reconstruire
make docker-clean
make docker-build
make docker-up
```

### Clé API non configurée

```bash
# Vérifier la configuration
cat .env | grep MISTRAL_API_KEY

# Si elle contient encore "your_mistral_api_key_here", éditez le fichier
nano .env
```

## 📁 Structure du projet

```
mistral_project/
├── README.md              # Documentation principale
├── setup.sh              # Script de setup automatique
├── validate-setup.sh     # Validation post-clone
├── docker-start.sh       # Démarrage Docker
├── docker-stop.sh        # Arrêt Docker
├── docker-compose.yml    # Orchestration Docker
├── Dockerfile.backend    # Image backend
├── Dockerfile.frontend   # Image frontend
├── nginx.conf            # Configuration nginx
├── .env.example          # Template de configuration
├── requirements.txt      # Dépendances Python
├── Makefile              # Commandes automatisées
├── back_end/             # Code backend FastAPI
├── front_end/            # Code frontend React
└── data/                 # Données vectorielles
```

## 📚 Documentation

- [🚀 Démarrage rapide](QUICK_START.md)
- [🐳 Guide Docker](DOCKER_README.md)
- [🚀 Déploiement](DEPLOYMENT.md)
- [🎨 Thème Mistral](THEME_MISTRAL.md)

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez la section dépannage ci-dessus
2. Vérifiez les logs : `make docker-logs`
3. Relancez la validation : `./validate-setup.sh`
4. Consultez la documentation complète

---

**🎉 Bienvenue dans l'écosystème Mistral Chatbot !**
