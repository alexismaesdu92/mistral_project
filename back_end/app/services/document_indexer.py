"""
Service d'indexation des documents markdown dans la base vectorielle.
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import hashlib

from app.services.vector_service import VectorService
from app.services.text_chunker import MarkdownChunker, TextChunk, DocumentIndexer


class DocumentIndexingService:
    """
    Service principal pour indexer les documents markdown dans ChromaDB.
    """
    
    def __init__(
        self,
        vector_service: Optional[VectorService] = None,
        chunker: Optional[MarkdownChunker] = None,
        data_dir: str = "data/scraping"
    ):

        self.vector_service = vector_service or VectorService(
            collection_name='mistral_docs',
            persist_directory="data/mistral_doc"
        )
        self.chunker = chunker or MarkdownChunker(
            chunk_size=1000,
            chunk_overlap=200,
            min_chunk_size=100
        )

        self.data_dir = Path(data_dir)
        self.index_metadata_file = Path("data/mistral_doc/index_metadata.json")
        
    def find_markdown_files(self) -> List[Path]:
        """Trouve tous les fichiers markdown dans le répertoire de données."""
        if not self.data_dir.exists():
            print(f"Le répertoire {self.data_dir} n'existe pas.")
            return []
        
        markdown_files = list(self.data_dir.rglob("*.md"))
        print(f"Trouvé {len(markdown_files)} fichiers markdown.")
        return markdown_files
    
    def load_index_metadata(self) -> Dict[str, Any]:
        """Charge les métadonnées d'indexation existantes."""
        if self.index_metadata_file.exists():
            try:
                with open(self.index_metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des métadonnées: {e}")
        
        return {
            "indexed_files": {},
            "total_chunks": 0,
            "last_update": None
        }
    
    def save_index_metadata(self, metadata: Dict[str, Any]):
        """Sauvegarde les métadonnées d'indexation."""
        self.index_metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.index_metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des métadonnées: {e}")
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calcule le hash SHA256 d'un fichier."""
        try:
            content = file_path.read_text(encoding='utf-8')
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        except Exception as e:
            print(f"Erreur lors du calcul du hash pour {file_path}: {e}")
            return ""
    
    def file_needs_reindexing(self, file_path: Path, metadata: Dict[str, Any]) -> bool:
        """Vérifie si un fichier doit être réindexé."""
        file_key = str(file_path.relative_to(self.data_dir))
        
        if file_key not in metadata["indexed_files"]:
            return True
        
        current_hash = self.get_file_hash(file_path)
        stored_hash = metadata["indexed_files"][file_key].get("hash", "")
        
        return current_hash != stored_hash
    
    async def index_file(self, file_path: Path) -> List[str]:
        """
        Indexe un fichier markdown spécifique.
        
        Args:
            file_path: Chemin vers le fichier à indexer
            
        Returns:
            Liste des IDs des chunks créés
        """
        print(f"Indexation de {file_path.name}...")
        

        chunks = self.chunker.chunk_markdown_file(file_path)
        
        if not chunks:
            print(f"Aucun chunk généré pour {file_path}")
            return []
        
        # Générer les IDs et préparer les données
        chunk_ids = []
        texts = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = DocumentIndexer.generate_chunk_id(chunk, i)
            chunk.chunk_id = chunk_id
            chunk_ids.append(chunk_id)
            
            # Ajouter les métadonnées au texte pour un meilleur contexte
            enhanced_text = self._enhance_chunk_text(chunk)
            texts.append(enhanced_text)
        
        try:
            # Indexer par batch pour l'efficacité
            await self.vector_service.add_batch(texts, chunk_ids)
            print(f"{len(chunks)} chunks indexed for {file_path.name}")
            return chunk_ids
            
        except Exception as e:
            print(f" Error during indexation {file_path}: {e}")
            return []
    
    def _enhance_chunk_text(self, chunk: TextChunk) -> str:
        """Améliore le texte du chunk avec du contexte des métadonnées."""
        enhanced_text = chunk.content
        
        # Ajouter le titre de la section si disponible
        section_header = chunk.metadata.get('section_header', '')
        if section_header and section_header not in enhanced_text:
            enhanced_text = f"Section: {section_header}\n\n{enhanced_text}"
        
        # Ajouter le titre du document si disponible
        doc_title = chunk.metadata.get('title', '')
        if doc_title and doc_title not in enhanced_text and doc_title != section_header:
            enhanced_text = f"Document: {doc_title}\n{enhanced_text}"
        
        return enhanced_text
    
    async def remove_file_chunks(self, file_path: Path, metadata: Dict[str, Any]):
        """Supprime les chunks d'un fichier de l'index."""
        file_key = str(file_path.relative_to(self.data_dir))
        
        if file_key in metadata["indexed_files"]:
            chunk_ids = metadata["indexed_files"][file_key].get("chunk_ids", [])
            
            for chunk_id in chunk_ids:
                try:
                    self.vector_service.delete_document(chunk_id)
                except Exception as e:
                    print(f"Erreur lors de la suppression du chunk {chunk_id}: {e}")
            
            print(f"Supprimé {len(chunk_ids)} chunks pour {file_path.name}")
    
    async def index_all_documents(self, force_reindex: bool = False) -> Dict[str, Any]:
        """
        Indexe tous les documents markdown.
        
        Args:
            force_reindex: Si True, réindexe tous les fichiers même s'ils n'ont pas changé
            
        Returns:
            Statistiques d'indexation
        """
        print("Begin indexing")
        
        # Charger les métadonnées existantes
        metadata = self.load_index_metadata()
        
        # Trouver tous les fichiers markdown
        markdown_files = self.find_markdown_files()
        
        if not markdown_files:
            print("no file markdown found.")
            return {"total_files": 0, "indexed_files": 0, "total_chunks": 0}
        
        stats = {
            "total_files": len(markdown_files),
            "indexed_files": 0,
            "skipped_files": 0,
            "total_chunks": 0,
            "errors": []
        }
        
        for file_path in tqdm(markdown_files, desc="Indexation des fichiers"):
            try:
                file_key = str(file_path.relative_to(self.data_dir))
                
                if not force_reindex and not self.file_needs_reindexing(file_path, metadata):
                    print(f"File {file_path.name} up to date, ignored.")
                    stats["skipped_files"] += 1
                    continue
                

                if file_key in metadata["indexed_files"]:
                    await self.remove_file_chunks(file_path, metadata)
                

                chunk_ids = await self.index_file(file_path)
                
                if chunk_ids:
                    metadata["indexed_files"][file_key] = {
                        "hash": self.get_file_hash(file_path),
                        "chunk_ids": chunk_ids,
                        "chunk_count": len(chunk_ids),
                        "last_indexed": asyncio.get_event_loop().time()
                    }
                    
                    stats["indexed_files"] += 1
                    stats["total_chunks"] += len(chunk_ids)
                else:
                    stats["errors"].append(f"Échec de l'indexation de {file_path}")
                
            except Exception as e:
                error_msg = f"Erreur avec {file_path}: {e}"
                print(f"{error_msg}")
                stats["errors"].append(error_msg)
        

        metadata["total_chunks"] = sum(
            file_info["chunk_count"] 
            for file_info in metadata["indexed_files"].values()
        )
        metadata["last_update"] = asyncio.get_event_loop().time()
        
        self.save_index_metadata(metadata)
        
        # Afficher les statistiques finales
        print("\nStatistiques d'indexation:")
        print(f"   Fichiers traités: {stats['indexed_files']}/{stats['total_files']}")
        print(f"   Fichiers ignorés: {stats['skipped_files']}")
        print(f"   Total chunks créés: {stats['total_chunks']}")
        print(f"   Erreurs: {len(stats['errors'])}")
        
        if stats["errors"]:
            print("\n❌ Erreurs rencontrées:")
            for error in stats["errors"][:5]:  # Afficher seulement les 5 premières
                print(f"   - {error}")
            if len(stats["errors"]) > 5:
                print(f"   ... et {len(stats['errors']) - 5} autres erreurs")
        
        print(f"\n✅ Indexation terminée! Base vectorielle prête à l'usage.")
        
        return stats
    
    async def search_documents(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Recherche dans les documents indexés.
        
        Args:
            query: Requête de recherche
            n_results: Nombre de résultats à retourner
            
        Returns:
            Résultats de recherche avec métadonnées
        """
        return await self.vector_service.search(query, n_results)



