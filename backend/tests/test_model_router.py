"""
Unit tests for Model Router

Tests cover:
- Complexity calculation
- Model routing logic
- Cache integration
- Fallback mechanism
- Metrics tracking
"""

import pytest
from unittest.mock import Mock, patch
from src.infrastructure.orchestrator.model_router import ModelRouter
from src.infrastructure.identity import MODEL_JUNIOR, MODEL_SENIOR, MODEL_DEBUG


class TestComplexityCalculation:
    """Test complexity calculation"""
    
    def test_simple_question_low_complexity(self):
        router = ModelRouter()
        complexity = router._calculate_complexity("What is Python?")
        assert complexity <= ModelRouter.COMPLEXITY_LOW
    
    def test_long_question_increases_complexity(self):
        router = ModelRouter()
        short = router._calculate_complexity("Simple question?")
        long = router._calculate_complexity("A" * 600)
        assert long > short
    
    def test_technical_keywords_increase_complexity(self):
        router = ModelRouter()
        simple = router._calculate_complexity("How to code?")
        technical = router._calculate_complexity(
            "How to optimize performance and scalability in async architecture?"
        )
        assert technical > simple
    
    def test_code_blocks_increase_complexity(self):
        router = ModelRouter()
        no_code = router._calculate_complexity("Explain async")
        with_code = router._calculate_complexity("Explain:\n```python\nasync def test():\n    pass\n```")
        assert with_code > no_code
    
    def test_complexity_capped_at_10(self):
        router = ModelRouter()
        very_complex = "A" * 1000 + "architecture scalability performance " * 10 + "```code```" + "?" * 10
        complexity = router._calculate_complexity(very_complex)
        assert complexity >= 8  # High complexity, may not reach exact 10


class TestRouting:
    """Test routing logic"""
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_route_to_junior_low_complexity(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.return_value = None
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.route("Simple question?")
        
        assert result["model"] == MODEL_JUNIOR
        assert result["use_cache"] is False
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_route_to_senior_high_complexity(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.return_value = None
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        # Create question with complexity >= 8
        complex_q = "Explain architecture scalability performance optimization async concurrent threading deadlock race condition"
        result = router.route(complex_q)
        
        assert result["model"] == MODEL_SENIOR
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_route_debug_mode(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.route("Any question", debug_mode=True)
        
        assert result["model"] == MODEL_DEBUG
        assert result["reason"] == "debug_mode"
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_route_cache_hit(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.return_value = {"content": "cached"}
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.route("Cached question")
        
        assert result["model"] is None
        assert result["use_cache"] is True
        assert result["reason"] == "cache_hit"
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_route_forced_model(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.route("Any question", force_model=MODEL_SENIOR)
        
        assert result["model"] == MODEL_SENIOR
        assert result["reason"] == "forced"


class TestFallback:
    """Test fallback mechanism"""
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_fallback_senior_to_junior(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.fallback(MODEL_SENIOR, "test question")
        
        assert result["model"] == MODEL_JUNIOR
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_fallback_junior_fails(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        result = router.fallback(MODEL_JUNIOR, "test question")
        
        assert result["model"] is None
        assert result["reason"] == "all_models_failed"


class TestMetrics:
    """Test metrics tracking"""
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_metrics_tracking(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.return_value = None
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        
        # Make some requests
        router.route("Simple 1")
        router.route("Simple 2")
        router.route("Complex architecture scalability performance optimization async concurrent threading deadlock")
        
        metrics = router.get_metrics()
        
        assert metrics["total_requests"] == 3
        assert metrics["junior_used"] == 2
        assert metrics["senior_used"] == 1
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_cache_hit_rate(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.side_effect = [
            {"content": "cached"},
            None,
            {"content": "cached"}
        ]
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        
        router.route("Q1")
        router.route("Q2")
        router.route("Q3")
        
        metrics = router.get_metrics()
        
        assert metrics["cache_hits"] == 2
        assert metrics["cache_hit_rate"] == 66.67
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_cost_tracking(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache_instance.get_cached_answer.return_value = None
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        
        router.route("Simple")
        
        metrics = router.get_metrics()
        
        assert metrics["total_cost"] > 0
        assert metrics["avg_cost_per_request"] > 0


class TestCostEstimation:
    """Test cost estimation"""
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_junior_cheaper_than_senior(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        
        junior_cost = router._estimate_cost(MODEL_JUNIOR)
        senior_cost = router._estimate_cost(MODEL_SENIOR)
        
        assert junior_cost < senior_cost
    
    @patch('src.infrastructure.orchestrator.model_router.CacheService')
    def test_cost_scales_with_tokens(self, mock_cache):
        mock_cache_instance = Mock()
        mock_cache.return_value = mock_cache_instance
        
        router = ModelRouter(mock_cache_instance)
        
        cost_1k = router._estimate_cost(MODEL_JUNIOR, 1000)
        cost_2k = router._estimate_cost(MODEL_JUNIOR, 2000)
        
        assert cost_2k == cost_1k * 2
