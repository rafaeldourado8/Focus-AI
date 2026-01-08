"""
Retrieval Service

Semantic search and context injection for RAG
"""

from typing import List, Dict, Optional
from src.infrastructure.rag.embeddings_service import EmbeddingsService
from src.infrastructure.rag.vector_store import VectorStore
from src.infrastructure.rag.document_processor import DocumentProcessor
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    """RAG retrieval service"""
    
    def __init__(self):
        # RAG disabled for production (requires sentence-transformers)
        # Uncomment when needed:
        # self.embeddings = EmbeddingsService()
        # self.vector_store = VectorStore()
        # self.processor = DocumentProcessor()
        logger.warning("RAG disabled - install sentence-transformers to enable")
    
    def index_code(self, code: str, language: str, source: str):
        """Index code for retrieval"""
        # Process into chunks
        chunks = self.processor.process_code(code, language, source)
        
        # Generate embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embeddings.embed_batch(texts)
        
        # Store in vector DB
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{source}_{i}"
            self.vector_store.add(chunk_id, chunk.content, embedding, chunk.metadata)
        
        logger.info(f"Indexed {len(chunks)} chunks from {source}")
    
    def index_documentation(self, text: str, framework: str, version: str = "latest"):
        """Index documentation"""
        chunks = self.processor.process_documentation(text, framework, version)
        
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embeddings.embed_batch(texts)
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{framework}_{version}_{i}"
            self.vector_store.add(chunk_id, chunk.content, embedding, chunk.metadata)
        
        logger.info(f"Indexed {len(chunks)} docs for {framework}")
    
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        language: Optional[str] = None,
        framework: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve relevant context for query
        
        Args:
            query: User query
            top_k: Number of results
            language: Filter by programming language
            framework: Filter by framework
        
        Returns:
            List of relevant chunks with scores
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed(query)
        
        # Build filters
        filters = {}
        if language:
            filters["language"] = language
        if framework:
            filters["framework"] = framework
        
        # Search vector store
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k * 2,  # Get more for re-ranking
            filter_metadata=filters if filters else None
        )
        
        # Re-rank by relevance
        reranked = self._rerank(query, results)
        
        return reranked[:top_k]
    
    def _rerank(self, query: str, results: List[Dict]) -> List[Dict]:
        """Re-rank results by query relevance"""
        # Simple re-ranking: boost exact keyword matches
        query_lower = query.lower()
        keywords = set(query_lower.split())
        
        for result in results:
            content_lower = result["content"].lower()
            
            # Count keyword matches
            matches = sum(1 for kw in keywords if kw in content_lower)
            
            # Boost score based on matches
            boost = 1.0 + (matches * 0.1)
            result["score"] = result["score"] * boost
        
        # Sort by boosted score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def build_context(self, query: str, language: Optional[str] = None) -> str:
        """
        Build context string for LLM prompt
        
        Args:
            query: User query
            language: Programming language filter
        
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, top_k=3, language=language)
        
        if not results:
            return ""
        
        context_parts = ["[RELEVANT DOCUMENTATION]\n"]
        
        for i, result in enumerate(results, 1):
            metadata = result["metadata"]
            content = result["content"]
            
            context_parts.append(f"\n--- Context {i} ---")
            context_parts.append(f"Source: {metadata.get('source', 'unknown')}")
            context_parts.append(f"Language: {metadata.get('language', 'N/A')}")
            context_parts.append(f"\n{content}\n")
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict:
        """Get retrieval statistics"""
        return {
            "total_documents": self.vector_store.count(),
            "embedding_dimension": self.embeddings.dimension
        }
