"""
Vector Store

Simple vector storage using Redis with RediSearch
"""

import redis
import json
import numpy as np
from typing import List, Dict, Any, Optional
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class VectorStore:
    """Simple vector store using Redis"""
    
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=False)
        self.index_name = "cerberus_docs"
    
    def add(self, chunk_id: str, content: str, embedding: List[float], metadata: Dict[str, Any]):
        """Add document chunk to store"""
        doc = {
            "content": content,
            "embedding": embedding,
            "metadata": metadata
        }
        
        key = f"doc:{chunk_id}"
        self.client.set(key, json.dumps(doc))
        logger.debug(f"Added document: {chunk_id}")
    
    def search(self, query_embedding: List[float], top_k: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query vector
            top_k: Number of results
            filter_metadata: Optional metadata filters
        
        Returns:
            List of matching documents with scores
        """
        results = []
        
        # Get all documents (simple implementation)
        keys = self.client.keys("doc:*")
        
        for key in keys:
            doc_json = self.client.get(key)
            if not doc_json:
                continue
            
            doc = json.loads(doc_json)
            
            # Apply metadata filters
            if filter_metadata:
                if not self._matches_filter(doc["metadata"], filter_metadata):
                    continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
            
            results.append({
                "content": doc["content"],
                "metadata": doc["metadata"],
                "score": similarity
            })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    
    def _matches_filter(self, metadata: Dict, filters: Dict) -> bool:
        """Check if metadata matches filters"""
        for key, value in filters.items():
            if metadata.get(key) != value:
                return False
        return True
    
    def count(self) -> int:
        """Count total documents"""
        return len(self.client.keys("doc:*"))
    
    def clear(self):
        """Clear all documents"""
        keys = self.client.keys("doc:*")
        if keys:
            self.client.delete(*keys)
        logger.info("Vector store cleared")
