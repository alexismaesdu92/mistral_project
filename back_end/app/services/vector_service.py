from mistralai import Mistral
from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any
import uuid


import chromadb

class Encoder:
    def __init__(
        self,
        api_key: str | None = None,
    ):
        load_dotenv()
        self.model_name = "mistral-embed"
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = Mistral(api_key=self.api_key)

    async def encode(self, text:str) -> list[float]:
        try:
            resp = await self.client.embeddings.create_async(
                model=self.model_name,
                inputs=[text]
            )
            embeddings = [item.embedding for item in resp.data]
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Error encoding text: {str(e)}")
        
    async def encode_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            resp = await self.client.embeddings.create_async(
                model=self.model_name,
                inputs=texts
            )
            embeddings = [item.embedding for item in resp.data]
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Error encoding batch of texts: {str(e)}")


class VectorService:
    def __init__(self, 
        collection_name:str = 'documents',
        persist_directory: str = None,
        encoder: Optional[Encoder]  = None
    ):
        if persist_directory is None:
            persist_directory = os.path.join("data", "doc")
        os.makedirs(persist_directory, exist_ok=True)

        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.encoder = encoder or Encoder()

        self.client = chromadb.PersistentClient(path=self.persist_directory)

        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        print(f"Collection {self.collection_name} ready to use")

    async def add(self, text: str, doc_id: Optional[str] = None) -> str:
        embeddings = await self.encoder.encode(text)

        if doc_id is None:
            doc_id = str(uuid.uuid4())

        self.collection.add(
            embeddings = embeddings,
            documents = [text],
            ids=[doc_id]
        )
        return doc_id

    async def add_batch(self, texts: list[str], doc_ids: Optional[list[str]] = None):
        embeddings = await self.encoder.encode_batch(texts)

        if doc_ids is None:
            doc_ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        self.collection.add(
            embeddings = embeddings,
            documents = texts,
            ids=doc_ids
        )
        return doc_ids
    

    async def search(
            self, 
            query: str, 
            n_results: int = 10,

    ) -> Dict[str, Any]:
        encoded_query = await self.encoder.encode(query)
        results = self.collection.query(
            query_embeddings=encoded_query[0],
            n_results=n_results,
            include=["documents", "distances"]

        )

        formated_results = []
        for i in range(len(results['ids'][0])):
            formated_results.append({
                "id": results['ids'][0][i],
                "text": results['documents'][0][i],
                "distance": results['distances'][0][i]
            })

        return {
            'query': query,
            'result': formated_results
        }
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        try:
            result = self.collection.get(
                ids=[doc_id],
                include=["documents"]
            )
            if not result['documents'] or len(result['documents'][0]) == 0:
                return None
            
            return {
                "id": doc_id,
                "text": result['documents'][0][0]
            }
        except:
            print(f"Error getting document {doc_id}")
            return None
    
    def delete_document(self, doc_id: str) -> bool:
        try:
            result = self.collection.get(ids=[doc_id])
            if not result["documents"] or len(result["documents"]) == 0:
                return False
            
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            return False
        

    async def update_document(self, doc_id: str, text: str) -> bool:
        try:
            # Vérifier d'abord si le document existe
            result = self.collection.get(ids=[doc_id])
            if not result["documents"] or len(result["documents"]) == 0:
                return False
            
            # Encoder le nouveau texte
            embeddings = await self.encoder.encode(text)
            
            # Mettre à jour le document
            self.collection.update(
                ids=[doc_id],
                embeddings=[embeddings[0]],  # Premier (et seul) embedding
                documents=[text]
            )
            return True
        except Exception as e:
            print(f"Error updating document: {str(e)}")
            return False
