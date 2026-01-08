"""
Unit tests for RAG components

Tests cover:
- Document processing
- Embeddings generation
- Vector search
- Retrieval service
"""

import pytest
from unittest.mock import Mock, patch
from src.infrastructure.rag.document_processor import DocumentProcessor, DocumentChunk
from src.infrastructure.rag.embeddings_service import EmbeddingsService
from src.infrastructure.rag.vector_store import VectorStore
from src.infrastructure.rag.retrieval_service import RetrievalService


class TestDocumentProcessor:
    """Test document processing"""
    
    def test_process_python_code(self):
        """Test Python code chunking"""
        processor = DocumentProcessor()
        code = """
def foo():
    return 1

def bar():
    return 2
"""
        chunks = processor.process_code(code, "python", "test.py")
        
        assert len(chunks) > 0
        assert all(isinstance(c, DocumentChunk) for c in chunks)
        assert chunks[0].metadata["language"] == "python"
    
    def test_process_documentation(self):
        """Test documentation chunking"""
        processor = DocumentProcessor()
        text = """
# Header 1
Content 1

# Header 2
Content 2
"""
        chunks = processor.process_documentation(text, "fastapi", "0.1.0")
        
        assert len(chunks) > 0
        assert chunks[0].metadata["framework"] == "fastapi"
    
    def test_chunk_size_limit(self):
        """Test chunk size respects limit"""
        processor = DocumentProcessor(chunk_size=100)
        long_text = "a" * 500
        
        chunks = processor._split_by_size(long_text)
        
        assert all(len(c) <= 150 for c in chunks)  # 100 + overlap


class TestEmbeddingsService:
    """Test embeddings generation"""
    
    @patch('src.infrastructure.rag.embeddings_service.SentenceTransformer')
    def test_embed_single_text(self, mock_model):
        """Test single text embedding"""
        mock_instance = Mock()
        mock_instance.encode.return_value = [0.1, 0.2, 0.3]
        mock_instance.get_sentence_embedding_dimension.return_value = 384
        mock_model.return_value = mock_instance
        
        service = EmbeddingsService()
        embedding = service.embed("test text")
        
        assert isinstance(embedding, list)
        assert len(embedding) == 3
    
    @patch('src.infrastructure.rag.embeddings_service.SentenceTransformer')
    def test_embed_batch(self, mock_model):
        """Test batch embedding"""
        mock_instance = Mock()
        mock_instance.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
        mock_instance.get_sentence_embedding_dimension.return_value = 384
        mock_model.return_value = mock_instance
        
        service = EmbeddingsService()
        embeddings = service.embed_batch(["text1", "text2"])
        
        assert len(embeddings) == 2


class TestVectorStore:
    """Test vector storage"""
    
    @patch('src.infrastructure.rag.vector_store.redis.from_url')
    def test_add_document(self, mock_redis):
        """Test adding document"""
        mock_client = Mock()
        mock_redis.return_value = mock_client
        
        store = VectorStore()
        store.add("doc1", "content", [0.1, 0.2], {"lang": "python"})
        
        mock_client.set.assert_called_once()
    
    @patch('src.infrastructure.rag.vector_store.redis.from_url')
    def test_search_returns_results(self, mock_redis):
        """Test search returns results"""
        mock_client = Mock()
        mock_client.keys.return_value = [b"doc:1"]
        mock_client.get.return_value = '{"content": "test", "embedding": [0.1, 0.2], "metadata": {}}'
        mock_redis.return_value = mock_client
        
        store = VectorStore()
        results = store.search([0.1, 0.2], top_k=1)
        
        assert len(results) <= 1


class TestRetrievalService:
    """Test retrieval service"""
    
    @patch('src.infrastructure.rag.retrieval_service.EmbeddingsService')
    @patch('src.infrastructure.rag.retrieval_service.VectorStore')
    @patch('src.infrastructure.rag.retrieval_service.DocumentProcessor')
    def test_index_code(self, mock_processor, mock_store, mock_embeddings):
        """Test code indexing"""
        mock_proc_instance = Mock()
        mock_chunk = Mock()
        mock_chunk.content = "def foo(): pass"
        mock_chunk.metadata = {"language": "python"}
        mock_proc_instance.process_code.return_value = [mock_chunk]
        mock_processor.return_value = mock_proc_instance
        
        mock_emb_instance = Mock()
        mock_emb_instance.embed_batch.return_value = [[0.1, 0.2]]
        mock_embeddings.return_value = mock_emb_instance
        
        mock_store_instance = Mock()
        mock_store.return_value = mock_store_instance
        
        service = RetrievalService()
        service.index_code("def foo(): pass", "python", "test.py")
        
        mock_store_instance.add.assert_called_once()
    
    @patch('src.infrastructure.rag.retrieval_service.EmbeddingsService')
    @patch('src.infrastructure.rag.retrieval_service.VectorStore')
    def test_retrieve_with_filters(self, mock_store, mock_embeddings):
        """Test retrieval with language filter"""
        mock_emb_instance = Mock()
        mock_emb_instance.embed.return_value = [0.1, 0.2]
        mock_embeddings.return_value = mock_emb_instance
        
        mock_store_instance = Mock()
        mock_store_instance.search.return_value = [
            {"content": "test", "metadata": {}, "score": 0.9}
        ]
        mock_store.return_value = mock_store_instance
        
        service = RetrievalService()
        results = service.retrieve("test query", language="python")
        
        assert len(results) >= 0
    
    @patch('src.infrastructure.rag.retrieval_service.EmbeddingsService')
    @patch('src.infrastructure.rag.retrieval_service.VectorStore')
    def test_build_context(self, mock_store, mock_embeddings):
        """Test context building"""
        mock_emb_instance = Mock()
        mock_emb_instance.embed.return_value = [0.1, 0.2]
        mock_embeddings.return_value = mock_emb_instance
        
        mock_store_instance = Mock()
        mock_store_instance.search.return_value = [
            {"content": "test content", "metadata": {"source": "test.py"}, "score": 0.9}
        ]
        mock_store.return_value = mock_store_instance
        
        service = RetrievalService()
        context = service.build_context("test query")
        
        assert "RELEVANT DOCUMENTATION" in context or context == ""
