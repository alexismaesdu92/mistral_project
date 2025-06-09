#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement de l'indexation.
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from services.text_chunker import MarkdownChunker
from services.document_indexer import DocumentIndexingService


async def test_chunker():
    """Teste le service de découpage de texte."""
    print("🧪 Test du service de découpage de texte...")
    
    # Créer un chunker
    chunker = MarkdownChunker(chunk_size=500, chunk_overlap=100)
    
    # Tester avec un fichier exemple
    test_files = list(Path("data/scraping").rglob("*.md"))
    
    if not test_files:
        print("❌ Aucun fichier markdown trouvé pour le test.")
        return False
    
    test_file = test_files[0]
    print(f"📄 Test avec le fichier: {test_file.name}")
    
    try:
        chunks = chunker.chunk_markdown_file(test_file)
        
        print(f"✅ {len(chunks)} chunks générés")
        
        if chunks:
            print(f"\n📋 Premier chunk:")
            print(f"   Taille: {len(chunks[0].content)} caractères")
            print(f"   Métadonnées: {chunks[0].metadata}")
            print(f"   Extrait: {chunks[0].content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du chunker: {e}")
        return False


async def test_small_indexing():
    """Teste l'indexation avec un petit échantillon."""
    print("\n🧪 Test d'indexation avec un échantillon...")
    
    try:
        # Créer un service d'indexation avec une collection de test
        from services.vector_service import VectorService
        
        test_vector_service = VectorService(
            collection_name='test_docs',
            persist_directory="data/doc_test"
        )
        
        indexer = DocumentIndexingService(
            vector_service=test_vector_service,
            data_dir="data/scraping"
        )
        
        # Trouver quelques fichiers pour le test
        markdown_files = indexer.find_markdown_files()
        
        if not markdown_files:
            print("❌ Aucun fichier markdown trouvé.")
            return False
        
        # Prendre seulement les 2 premiers fichiers pour le test
        test_files = markdown_files[:2]
        print(f"📁 Test avec {len(test_files)} fichiers:")
        for f in test_files:
            print(f"   - {f.name}")
        
        # Indexer chaque fichier
        total_chunks = 0
        for file_path in test_files:
            chunk_ids = await indexer.index_file(file_path)
            total_chunks += len(chunk_ids)
            print(f"   ✅ {file_path.name}: {len(chunk_ids)} chunks")
        
        print(f"\n📊 Total: {total_chunks} chunks indexés")
        
        # Tester une recherche
        print("\n🔍 Test de recherche...")
        results = await indexer.search_documents("Mistral AI", n_results=3)
        
        if results['result']:
            print(f"✅ {len(results['result'])} résultats trouvés")
            
            best_result = results['result'][0]
            print(f"   Meilleur résultat (score: {1 - best_result['distance']:.3f}):")
            print(f"   {best_result['text'][:150]}...")
        else:
            print("⚠️ Aucun résultat trouvé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'indexation: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_vector_service():
    """Teste le service vectoriel de base."""
    print("\n🧪 Test du service vectoriel...")
    
    try:
        from services.vector_service import VectorService
        
        # Créer un service de test
        vector_service = VectorService(
            collection_name='simple_test',
            persist_directory="data/doc_test"
        )
        
        # Tester l'ajout d'un document simple
        test_text = "Mistral AI est une entreprise française spécialisée dans l'intelligence artificielle."
        doc_id = await vector_service.add(test_text, "test_doc_1")
        
        print(f"✅ Document ajouté avec l'ID: {doc_id}")
        
        # Tester la recherche
        results = await vector_service.search("intelligence artificielle française", n_results=1)
        
        if results['result']:
            result = results['result'][0]
            print(f"✅ Recherche réussie (score: {1 - result['distance']:.3f})")
            print(f"   Texte trouvé: {result['text']}")
        else:
            print("❌ Aucun résultat trouvé")
            return False
        
        # Tester la récupération du document
        doc = vector_service.get_document(doc_id)
        if doc:
            print(f"✅ Document récupéré: {doc['text'][:50]}...")
        else:
            print("❌ Impossible de récupérer le document")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du service vectoriel: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Lance tous les tests."""
    print("🚀 Lancement des tests d'indexation...\n")
    
    # Vérifier les prérequis
    if not Path("data/scraping").exists():
        print("❌ Le répertoire 'data/scraping' n'existe pas.")
        print("   Exécutez d'abord le scraping des documents.")
        return
    
    # Tests
    tests = [
        ("Service vectoriel de base", test_vector_service),
        ("Service de découpage", test_chunker),
        ("Indexation échantillon", test_small_indexing),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 {test_name}")
        print('='*50)
        
        try:
            success = await test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
                
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
            results.append((test_name, False))
    
    # Résumé
    print(f"\n{'='*50}")
    print("📊 RÉSUMÉ DES TESTS")
    print('='*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés! L'indexation est prête à être utilisée.")
        print("\n💡 Prochaines étapes:")
        print("   1. Lancez l'indexation complète: python index_documents.py")
        print("   2. Testez la recherche: python index_documents.py --search 'votre requête'")
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué. Vérifiez la configuration.")


if __name__ == "__main__":
    asyncio.run(main())
