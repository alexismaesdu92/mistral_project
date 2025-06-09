import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextChunk:
    """Représente un chunk de texte avec ses métadonnées."""
    content: str
    metadata: Dict[str, Any]
    chunk_id: Optional[str] = None


class MarkdownChunker:
    """
    Découpe les documents markdown en chunks optimaux pour l'indexation vectorielle.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_markdown_file(self, file_path: Path) -> List[TextChunk]:
        try:
            content = file_path.read_text(encoding='utf-8')
            return self.chunk_markdown_content(content, file_path)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
            return []
    
    def chunk_markdown_content(self, content: str, file_path: Path) -> List[TextChunk]:
        content = self._clean_markdown(content)
        base_metadata = self._extract_file_metadata(file_path, content)
        sections = self._split_by_headers(content)
        
        chunks = []
        for section in sections:
            section_chunks = self._chunk_section(section, base_metadata)
            chunks.extend(section_chunks)
        
        return chunks
    
    def _clean_markdown(self, content: str) -> str:
        """Nettoie le contenu markdown."""
        # Supprimer les liens de navigation
        content = re.sub(r'\* \[.*?\]\(.*?\)\n', '', content)
        
        # Nettoyer les espaces multiples
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Supprimer les lignes de navigation communes
        navigation_patterns = [
            r'On this page\n',
            r'Next\n.*?\n',
            r'Previous\n.*?\n',
            r'\[Edit this page\].*?\n'
        ]
        
        for pattern in navigation_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        return content.strip()
    
    def _extract_file_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extrait les métadonnées du fichier."""
        # Extraire le titre principal
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # Construire le chemin relatif depuis data/scraping
        try:
            relative_path = file_path.relative_to(Path("data/scraping"))
        except ValueError:
            relative_path = file_path
        
        return {
            "source_file": str(relative_path),
            "file_name": file_path.name,
            "title": title,
            "doc_type": "mistral_documentation",
            "language": "fr" if "bienvenue" in content.lower() else "en"
        }
    
    def _split_by_headers(self, content: str) -> List[Dict[str, Any]]:
        """Découpe le contenu par headers markdown."""
        sections = []
        
        # Pattern pour détecter les headers
        header_pattern = r'^(#{1,6})\s+(.+)$'
        
        lines = content.split('\n')
        current_section = {
            'header': '',
            'level': 0,
            'content': '',
            'start_line': 0
        }
        
        for i, line in enumerate(lines):
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Sauvegarder la section précédente si elle a du contenu
                if current_section['content'].strip():
                    sections.append(current_section.copy())
                
                # Commencer une nouvelle section
                level = len(header_match.group(1))
                header_text = header_match.group(2)
                
                current_section = {
                    'header': header_text,
                    'level': level,
                    'content': line + '\n',
                    'start_line': i
                }
            else:
                current_section['content'] += line + '\n'
        
        # Ajouter la dernière section
        if current_section['content'].strip():
            sections.append(current_section)
        
        return sections
    
    def _chunk_section(self, section: Dict[str, Any], base_metadata: Dict[str, Any]) -> List[TextChunk]:
        """Découpe une section en chunks."""
        content = section['content'].strip()
        
        if len(content) <= self.chunk_size:
            # La section entière tient dans un chunk
            metadata = base_metadata.copy()
            metadata.update({
                'section_header': section['header'],
                'section_level': section['level'],
                'chunk_type': 'complete_section'
            })
            
            return [TextChunk(content=content, metadata=metadata)]
        
        chunks = []
        sentences = self._split_into_sentences(content)
        
        current_chunk = ""
        current_sentences = []
        
        for sentence in sentences:
            # Vérifier si ajouter cette phrase dépasserait la taille limite
            if len(current_chunk + sentence) > self.chunk_size and current_chunk:
                # Créer un chunk avec le contenu actuel
                metadata = base_metadata.copy()
                metadata.update({
                    'section_header': section['header'],
                    'section_level': section['level'],
                    'chunk_type': 'partial_section',
                    'sentence_count': len(current_sentences)
                })
                
                chunks.append(TextChunk(content=current_chunk.strip(), metadata=metadata))
                
                # Commencer un nouveau chunk avec chevauchement
                overlap_text = self._get_overlap_text(current_chunk, self.chunk_overlap)
                current_chunk = overlap_text + sentence
                current_sentences = [sentence]
            else:
                current_chunk += sentence
                current_sentences.append(sentence)
        
        # Ajouter le dernier chunk s'il a une taille suffisante
        if len(current_chunk.strip()) >= self.min_chunk_size:
            metadata = base_metadata.copy()
            metadata.update({
                'section_header': section['header'],
                'section_level': section['level'],
                'chunk_type': 'partial_section',
                'sentence_count': len(current_sentences)
            })
            
            chunks.append(TextChunk(content=current_chunk.strip(), metadata=metadata))
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Découpe le texte en phrases."""
        # Pattern pour détecter les fins de phrases
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=\n\n)'
        
        sentences = re.split(sentence_pattern, text)
        
        # Nettoyer et filtrer les phrases vides
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Ignorer les phrases trop courtes
                cleaned_sentences.append(sentence + ' ')
        
        return cleaned_sentences
    
    def _get_overlap_text(self, text: str, overlap_size: int) -> str:
        """Récupère le texte de chevauchement à la fin d'un chunk."""
        if len(text) <= overlap_size:
            return text
        
        # Essayer de couper à une phrase complète
        overlap_text = text[-overlap_size:]
        
        # Chercher le début d'une phrase dans le chevauchement
        sentence_start = re.search(r'[.!?]\s+[A-Z]', overlap_text)
        if sentence_start:
            return overlap_text[sentence_start.end()-1:]
        
        return overlap_text


class DocumentIndexer:
    """
    Classe utilitaire pour indexer des documents avec métadonnées.
    """
    
    @staticmethod
    def generate_chunk_id(chunk: TextChunk, index: int) -> str:
        """Génère un ID unique pour un chunk."""
        source_file = chunk.metadata.get('source_file', 'unknown')
        section = chunk.metadata.get('section_header', 'no_section')
        
        # Créer un ID basé sur le fichier, la section et l'index
        clean_file = re.sub(r'[^\w\-_.]', '_', source_file)
        clean_section = re.sub(r'[^\w\-_]', '_', section)[:50]  # Limiter la longueur
        
        return f"{clean_file}_{clean_section}_{index:03d}"
    
    @staticmethod
    def chunk_to_document_format(chunk: TextChunk) -> Dict[str, Any]:
        """Convertit un chunk en format pour la base vectorielle."""
        return {
            'id': chunk.chunk_id,
            'text': chunk.content,
            'metadata': chunk.metadata
        }
