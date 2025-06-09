# 🤖 Mistral Chatbot

Une application de chat moderne utilisant l'API Mistral AI avec interface React et backend FastAPI.

![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![React](https://img.shields.io/badge/React-19.1.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)

## 🚀 Démarrage rapide

### Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé
- Clé API Mistral AI ([obtenir ici](https://console.mistral.ai))

### Installation en 2 étapes

```bash
# 1. Cloner le projet
git clone <votre-repo-url>
cd mistral_project

# 2. Setup automatique
./setup.sh
```

### Installation manuelle

```bash
# 1. Validation post-clone
./validate-setup.sh

# 2. Configuration
cp .env.example .env
# Éditer .env et ajouter votre clé API Mistral

# 3. Démarrage
./docker-start.sh
```

### Accès à l'application
- **Interface** : http://localhost:3000
- **API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🎨 Fonctionnalités

- ✅ **Interface moderne** aux couleurs Mistral AI
- ✅ **Chat en temps réel** avec l'API Mistral
- ✅ **Support Markdown** avec coloration syntaxique
- ✅ **Mode RAG** pour la recherche documentaire
- ✅ **Responsive design** pour mobile et desktop
- ✅ **Containerisation Docker** complète

## 🛠️ Commandes utiles

```bash
# Démarrer l'application
make docker-up

# Voir les logs
make docker-logs

# Arrêter l'application
make docker-down

# Aide complète
make help
```

## 📁 Structure du projet

```
mistral_project/
├── back_end/           # Backend FastAPI
├── front_end/          # Frontend React
├── data/              # Données vectorielles
├── docker-compose.yml # Orchestration Docker
├── Dockerfile.*       # Images Docker
└── docs/              # Documentation
```

## 🔧 Configuration

### Variables d'environnement (.env)
```env
MISTRAL_API_KEY=your_api_key_here
MISTRAL_MODEL=mistral-medium
FRONTEND_PORT=3000
BACKEND_PORT=8000
```

## 🐛 Dépannage

### Docker daemon non démarré
```bash
# macOS
open -a Docker

# Vérifier
docker info
```

### Ports occupés
```bash
# Vérifier les ports
lsof -i :3000
lsof -i :8000
```

### Clé API manquante
```bash
# Vérifier la configuration
cat .env | grep MISTRAL_API_KEY
```

## 📚 Documentation

- [🚀 Démarrage rapide](QUICK_START.md)
- [🐳 Guide Docker](DOCKER_README.md)
- [🚀 Déploiement](DEPLOYMENT.md)
- [🎨 Thème Mistral](THEME_MISTRAL.md)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

- 📖 [Documentation complète](DOCKER_README.md)
- 🐛 [Signaler un bug](https://github.com/votre-repo/issues)
- 💬 [Discussions](https://github.com/votre-repo/discussions)

---

**Développé avec ❤️ pour la communauté Mistral AI**
