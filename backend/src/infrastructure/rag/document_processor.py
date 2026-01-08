"""
Document Processor

Handles document chunking and metadata extraction
"""

from typing import List, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)


class DocumentChunk:
    """Document chunk with metadata"""
    
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata
        self.embedding = None


class DocumentProcessor:
    """Process and chunk documents for RAG"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_code(self, code: str, language: str, source: str = "unknown") -> List[DocumentChunk]:
        """
        Process code into chunks
        
        Args:
            code: Source code
            language: Programming language
            source: Source identifier (file path, URL, etc)
        
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        
        # Split by functions/classes for code
        if language in ["python", "javascript", "typescript"]:
            code_chunks = self._split_by_functions(code, language)
        else:
            code_chunks = self._split_by_size(code)
        
        for i, chunk_text in enumerate(code_chunks):
            chunk = DocumentChunk(
                content=chunk_text,
                metadata={
                    "type": "code",
                    "language": language,
                    "source": source,
                    "chunk_index": i,
                    "total_chunks": len(code_chunks)
                }
            )
            chunks.append(chunk)
        
        logger.info(f"Processed {len(chunks)} chunks from {source}")
        return chunks
    
    def process_documentation(self, text: str, framework: str, version: str = "latest") -> List[DocumentChunk]:
        """Process documentation text"""
        chunks = []
        
        # Split by sections (headers)
        sections = self._split_by_headers(text)
        
        for i, section in enumerate(sections):
            chunk = DocumentChunk(
                content=section,
                metadata={
                    "type": "documentation",
                    "framework": framework,
                    "version": version,
                    "chunk_index": i
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def _split_by_functions(self, code: str, language: str) -> List[str]:
        """Split code by function/class definitions"""
        chunks = []
        
        if language == "python":
            # Split by def/class
            pattern = r'((?:^|\n)(?:def|class)\s+\w+.*?(?=\n(?:def|class)\s+|\Z))'
            matches = re.findall(pattern, code, re.DOTALL | re.MULTILINE)
            chunks = [m.strip() for m in matches if m.strip()]
        
        elif language in ["javascript", "typescript"]:
            # Split by function/class
            pattern = r'((?:^|\n)(?:function|class|const\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>).*?(?=\n(?:function|class|const\s+\w+\s*=)|\Z))'
            matches = re.findall(pattern, code, re.DOTALL | re.MULTILINE)
            chunks = [m.strip() for m in matches if m.strip()]
        
        # Fallback to size-based splitting
        if not chunks:
            chunks = self._split_by_size(code)
        
        return chunks
    
    def _split_by_headers(self, text: str) -> List[str]:
        """Split text by markdown headers"""
        # Split by # headers
        pattern = r'((?:^|\n)#{1,3}\s+.*?(?=\n#{1,3}\s+|\Z))'
        matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
        
        if matches:
            return [m.strip() for m in matches if m.strip()]
        
        return self._split_by_size(text)
    
    def _split_by_size(self, text: str) -> List[str]:
        """Split text by size with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            start = end - self.chunk_overlap
        
        return chunks
