import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from services.vector_service import Encoder

async def test_embeddings():
    # Créer une instance du service
    encoder = Encoder()
    
    # Tester avec quelques phrases
    texts = [
        "Mistral AI est une entreprise française spécialisée dans l'IA générative.",
        "Comment utiliser l'API Mistral pour générer du texte?",
    ]
    
    print("Génération d'embeddings...")
    
    try:
        # Encoder le premier texte
        embeddings = await encoder.encode(texts[0])
        
        print(f"✓ Premier embedding généré")
        print(f"✓ Dimension: {len(embeddings[0])}")
        
        # Encoder le deuxième texte
        embeddings2 = await encoder.encode(texts[1])
        print(f"✓ Deuxième embedding généré")
        
        print("\n✅ Test réussi! Le service d'embeddings fonctionne correctement.")
        return True
        
    except Exception as e:
        print(f"\n Erreur lors de la génération d'embeddings: {str(e)}")
        return False

if __name__ == "__main__":
    # Exécuter le test de manière asynchrone
    success = asyncio.run(test_embeddings())
    
    if not success:
        print("Vérifiez votre clé API et votre connexion internet.")