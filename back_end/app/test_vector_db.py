import asyncio
import sys
from pathlib import Path
import json

# Ajouter le répertoire parent au PYTHONPATH
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from services.vector_service import VectorService

async def test_vector_db():
    print("=" * 50)
    print("TEST DE LA BASE DE DONNÉES VECTORIELLE")
    print("=" * 50)
    
    # Initialiser le service
    db = VectorService(collection_name="test_collection")
    
    # 1. Ajouter un document
    print("\n1. Ajout d'un document")
    print("-" * 30)
    
    doc_text = "Mistral AI est une entreprise française spécialisée dans l'IA générative."
 
    doc_id = await db.add(doc_text)
    print(f"Document ajouté avec l'ID: {doc_id}")
    
    # 2. Ajouter plusieurs documents
    print("\n2. Ajout de plusieurs documents")
    print("-" * 30)
    
    texts = [
        "Les modèles de langage sont utilisés pour comprendre et générer du texte.",
        "L'API Mistral permet d'accéder à des modèles de langage puissants.",
        "Les embeddings sont des représentations vectorielles du texte.",
        "La recherche sémantique permet de trouver des documents par leur signification."
    ]
    
    
    doc_ids = await db.add_batch(texts)
    print(f"Documents ajoutés avec les IDs: {doc_ids}")
    
    # 3. Rechercher des documents
    print("\n3. Recherche de documents")
    print("-" * 30)
    
    query = "Comment fonctionne l'API de Mistral?"
    print(f"Requête: '{query}'")
    
    results = await db.search(query, n_results=3)
    
    print("\nRésultats de la recherche:")
    for i, result in enumerate(results['result']):
        print(f"{i+1}. Distance: {1-result['distance']:.4f}")
        print(f"   ID: {result['id']}")
        print(f"   Texte: {result['text']}")
        print()
    
    # 4. Récupérer un document par ID
    print("\n4. Récupération d'un document par ID")
    print("-" * 30)
    
    doc = db.get_document(doc_ids[0])
    print(f"Document récupéré:")
    print(f"ID: {doc['id']}")
    print(f"Texte: {doc['text']}")
    

    
    print("\n" + "=" * 50)
    print("✅ TEST TERMINÉ AVEC SUCCÈS!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_vector_db())