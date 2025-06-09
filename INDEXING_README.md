# 📚 Système d'Indexation Vectorielle - Documentation Mistral AI

Ce système permet d'indexer automatiquement tous les fichiers markdown de la documentation Mistral AI dans une base vectorielle ChromaDB pour permettre des recherches sémantiques rapides et précises.

## 🏗️ Architecture

### Composants principaux

1. **`VectorService`** (`vector_service.py`)
   - Interface avec ChromaDB
   - Gestion des embeddings via l'API Mistral
   - Opérations CRUD sur les documents vectorisés

2. **`MarkdownChunker`** (`text_chunker.py`)
   - Découpage intelligent des documents markdown
   - Préservation du contexte (sections, titres)
   - Gestion du chevauchement entre chunks

3. **`DocumentIndexingService`** (`document_indexer.py`)
   - Orchestration de l'indexation
   - Gestion incrémentale (détection des changements)
   - Métadonnées et statistiques

4. **Scripts utilitaires**
   - `index_documents.py` : Script principal d'indexation
   - `test_indexing.py` : Tests et validation

## 🚀 Installation et Configuration

### 1. Installer les dépendances

```bash
# Installer les dépendances du projet
pip install -e ".[dev]"

# Ou installer manuellement les dépendances principales
pip install chromadb tqdm beautifulsoup4 markdownify python-slugify
```

### 2. Configuration de l'API Mistral

Créez un fichier `.env` à la racine du projet :

```env
MISTRAL_API_KEY=votre_clé_api_mistral
```

### 3. Vérifier la structure des données

Assurez-vous que les fichiers markdown sont dans `data/scraping/` :

```
data/
├── scraping/
│   ├── docs.mistral.ai/
│   │   ├── index.md
│   │   ├── capabilities/
│   │   ├── guides/
│   │   └── ...
│   └── manifest.csv
└── doc/  # Sera créé automatiquement pour ChromaDB
```

## 🔧 Utilisation

### Tests préliminaires

Avant la première indexation, lancez les tests :

```bash
cd back_end/app
python test_indexing.py
```

### Indexation complète

```bash
cd back_end/app

# Première indexation (complète)
python index_documents.py

# Réindexation forcée de tous les fichiers
python index_documents.py --force

# Indexation incrémentale (seulement les fichiers modifiés)
python index_documents.py
```

### Test de recherche

```bash
# Rechercher dans les documents indexés
python index_documents.py --search "Mistral Large"
python index_documents.py --search "fine-tuning"
python index_documents.py --search "comment utiliser l'API"
```

### Statistiques

```bash
# Afficher les statistiques de l'index
python index_documents.py --stats
```

## 📊 Fonctionnalités

### Découpage intelligent

- **Par sections** : Respect de la hiérarchie markdown (H1, H2, H3...)
- **Taille optimale** : Chunks de ~1000 caractères avec chevauchement de 200
- **Contexte préservé** : Inclusion des titres de section et document
- **Métadonnées riches** : Fichier source, section, langue, type de contenu

### Indexation incrémentale

- **Détection des changements** : Hash SHA256 des fichiers
- **Mise à jour sélective** : Seuls les fichiers modifiés sont réindexés
- **Gestion des suppressions** : Nettoyage automatique des anciens chunks
- **Métadonnées persistantes** : Suivi de l'état d'indexation

### Recherche sémantique

- **Embeddings Mistral** : Utilisation du modèle `mistral-embed`
- **Recherche par similarité** : Scores de pertinence
- **Métadonnées contextuelles** : Informations sur la source des résultats
- **Résultats enrichis** : Texte + contexte + métadonnées

## 🔍 Utilisation dans le code

### Recherche simple

```python
from services.document_indexer import DocumentIndexingService

# Créer le service
indexer = DocumentIndexingService()

# Rechercher
results = await indexer.search_documents("Comment utiliser Mistral Large?", n_results=5)

for result in results['result']:
    print(f"Score: {1 - result['distance']:.3f}")
    print(f"Texte: {result['text'][:200]}...")
    print(f"Source: {result.get('metadata', {}).get('source_file', 'Unknown')}")
```

### Utilisation directe du VectorService

```python
from services.vector_service import VectorService

# Créer le service vectoriel
vector_service = VectorService(collection_name='mistral_docs')

# Rechercher
results = await vector_service.search("fine-tuning Mistral", n_results=3)

# Ajouter un nouveau document
doc_id = await vector_service.add("Nouveau contenu à indexer", "custom_doc_1")
```

## 📁 Structure des fichiers générés

```
data/
├── doc/                          # Base ChromaDB
│   ├── chroma.sqlite3           # Base de données SQLite
│   ├── index_metadata.json      # Métadonnées d'indexation
│   └── [uuid]/                  # Collections ChromaDB
└── doc_test/                    # Base de test (créée par les tests)
```

### Métadonnées d'indexation

Le fichier `data/doc/index_metadata.json` contient :

```json
{
  "indexed_files": {
    "docs.mistral.ai/index.md": {
      "hash": "a218b79321fed0bf...",
      "chunk_ids": ["docs_mistral_ai_index_md_Bienvenue_to_Mistral_AI_Documentation_001", ...],
      "chunk_count": 15,
      "last_indexed": 1704067200.0
    }
  },
  "total_chunks": 1247,
  "last_update": 1704067200.0
}
```

## 🎯 Optimisations et bonnes pratiques

### Paramètres de chunking

```python
# Configuration recommandée pour la documentation
chunker = MarkdownChunker(
    chunk_size=1000,      # Taille optimale pour les embeddings
    chunk_overlap=200,    # Chevauchement pour préserver le contexte
    min_chunk_size=100    # Éviter les chunks trop petits
)
```

### Gestion de la mémoire

- L'indexation traite les fichiers un par un
- Les embeddings sont générés par batch pour l'efficacité
- ChromaDB persiste automatiquement les données

### Performance

- **Première indexation** : ~2-3 minutes pour ~50 fichiers
- **Indexation incrémentale** : ~10-30 secondes
- **Recherche** : ~100-200ms par requête

## 🐛 Dépannage

### Erreurs communes

1. **"MISTRAL_API_KEY not set"**
   ```bash
   # Vérifier le fichier .env
   cat .env
   # Ou exporter directement
   export MISTRAL_API_KEY="votre_clé"
   ```

2. **"No markdown files found"**
   ```bash
   # Vérifier la structure des données
   ls -la data/scraping/
   # Relancer le scraping si nécessaire
   ```

3. **Erreurs ChromaDB**
   ```bash
   # Supprimer et recréer la base
   rm -rf data/doc/
   python index_documents.py --force
   ```

### Logs et debugging

```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Ou utiliser le mode verbose dans les scripts
python index_documents.py --force  # Affiche plus de détails
```

## 🔄 Intégration avec le chatbot

Le système d'indexation s'intègre parfaitement avec votre `MistralService` :

```python
# Dans votre chatbot
from services.document_indexer import DocumentIndexingService

class EnhancedMistralService(MistralService):
    def __init__(self):
        super().__init__()
        self.indexer = DocumentIndexingService()
    
    async def generate_response_with_context(self, prompt: str):
        # Rechercher du contexte pertinent
        context_results = await self.indexer.search_documents(prompt, n_results=3)
        
        # Construire le prompt avec contexte
        context = "\n".join([r['text'] for r in context_results['result']])
        enhanced_prompt = f"Contexte:\n{context}\n\nQuestion: {prompt}"
        
        # Générer la réponse
        return await self.generate_response(enhanced_prompt)
```

## 📈 Prochaines améliorations

- [ ] Interface web pour la gestion de l'index
- [ ] Support de formats additionnels (PDF, HTML)
- [ ] Recherche hybride (mots-clés + sémantique)
- [ ] Mise à jour en temps réel via webhooks
- [ ] Métriques et analytics de recherche
