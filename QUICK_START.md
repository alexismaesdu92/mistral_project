# 🚀 Démarrage rapide - Mistral Chatbot

## ⚡ En 3 étapes simples

### 1. 🔑 Configurer votre clé API

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer le fichier .env
nano .env  # ou votre éditeur préféré
```

**Important** : Remplacez `your_mistral_api_key_here` par votre vraie clé API Mistral.

**Obtenir une clé API** :
1. Allez sur https://console.mistral.ai
2. Créez un compte ou connectez-vous
3. Naviguez vers "API Keys"
4. Créez une nouvelle clé API
5. Copiez la clé dans votre fichier `.env`

### 2. 🐳 Démarrer avec Docker

```bash
# Démarrage automatique (recommandé)
./docker-start.sh

# OU avec make
make docker-up

# OU avec docker-compose
docker-compose up --build -d
```

### 3. 🌐 Accéder à l'application

- **Interface** : http://localhost:3000
- **API** : http://localhost:8000
- **Documentation** : http://localhost:8000/docs

## 🛠️ Commandes utiles

```bash
# Voir les logs
make docker-logs

# Arrêter l'application
make docker-down

# Redémarrer
make docker-restart

# Aide complète
make help
```

## 🐛 Problèmes courants

### Docker daemon non démarré
```bash
# Démarrer Docker Desktop
open -a Docker  # macOS
```

### Clé API manquante
```bash
# Vérifier le fichier .env
cat .env | grep MISTRAL_API_KEY
```

### Ports occupés
```bash
# Vérifier les ports
lsof -i :3000
lsof -i :8000
```

## 📚 Documentation complète

- **Docker** : `DOCKER_README.md`
- **Déploiement** : `DEPLOYMENT.md`
- **Aide** : `make help`

---

**🎉 C'est tout ! Votre application Mistral Chatbot est prête à l'emploi !**
