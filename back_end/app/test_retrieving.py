import asyncio

from .services.vector_service import VectorService


if __name__ == '__main__':
    vector_service = VectorService(collection_name="mistral_docs",
                                   persist_directory="data/mistral_doc")
    results = asyncio.run(vector_service.search("Comment utiliser l'API Mistral?", n_results=5))
    for result in results['result']:
        print("document id:", result['id'])
        print("text: ", result['text'])
        print("=====================================")
        print()