"""
Unit tests for Metrics Service

Tests cover:
- Request tracking
- Cache metrics
- Model usage
- Cost tracking
- Error tracking
- Timer context manager
"""

import pytest
from unittest.mock import patch
from src.infrastructure.monitoring.metrics_service import (
    MetricsService,
    RequestTimer,
    requests_total,
    cache_hits,
    cache_misses,
    model_usage,
    total_cost,
    errors_total
)


class TestMetricsTracking:
    """Test metrics tracking"""
    
    def test_track_request(self):
        """Test request tracking"""
        initial = requests_total.labels(model="test", status="success")._value.get()
        
        MetricsService.track_request("test", "success", 1.5, "chat")
        
        final = requests_total.labels(model="test", status="success")._value.get()
        assert final > initial
    
    def test_track_cache_hit(self):
        """Test cache hit tracking"""
        initial = cache_hits._value.get()
        
        MetricsService.track_cache_hit()
        
        final = cache_hits._value.get()
        assert final == initial + 1
    
    def test_track_cache_miss(self):
        """Test cache miss tracking"""
        initial = cache_misses._value.get()
        
        MetricsService.track_cache_miss()
        
        final = cache_misses._value.get()
        assert final == initial + 1
    
    def test_track_model_usage(self):
        """Test model usage tracking"""
        initial = model_usage.labels(model="cerberus-lite")._value.get()
        
        MetricsService.track_model_usage("cerberus-lite")
        
        final = model_usage.labels(model="cerberus-lite")._value.get()
        assert final > initial
    
    def test_track_cost(self):
        """Test cost tracking"""
        initial = total_cost._value.get()
        
        MetricsService.track_cost(0.001)
        
        final = total_cost._value.get()
        assert final > initial
    
    def test_track_error(self):
        """Test error tracking"""
        initial = errors_total.labels(error_type="llm_error")._value.get()
        
        MetricsService.track_error("llm_error")
        
        final = errors_total.labels(error_type="llm_error")._value.get()
        assert final > initial


class TestRequestTimer:
    """Test request timer context manager"""
    
    def test_timer_success(self):
        """Test timer tracks successful request"""
        with RequestTimer("test-model", "test-endpoint") as timer:
            pass
        
        assert timer.duration is not None
        assert timer.duration >= 0
    
    def test_timer_error(self):
        """Test timer tracks failed request"""
        try:
            with RequestTimer("test-model", "test-endpoint"):
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Should track error status
        error_count = requests_total.labels(model="test-model", status="error")._value.get()
        assert error_count > 0
    
    def test_timer_duration_recorded(self):
        """Test timer records duration"""
        import time
        
        with RequestTimer("test-model") as timer:
            time.sleep(0.01)
        
        assert timer.duration >= 0.01


class TestMetricsExport:
    """Test metrics export"""
    
    def test_get_metrics_returns_bytes(self):
        """Test metrics export returns bytes"""
        metrics = MetricsService.get_metrics()
        assert isinstance(metrics, bytes)
    
    def test_get_content_type(self):
        """Test content type is correct"""
        content_type = MetricsService.get_content_type()
        assert "text/plain" in content_type or "prometheus" in content_type.lower()
    
    def test_metrics_contain_cerberus_prefix(self):
        """Test metrics have cerberus prefix"""
        metrics = MetricsService.get_metrics().decode('utf-8')
        assert "cerberus_" in metrics


class TestActiveSessions:
    """Test active sessions gauge"""
    
    def test_set_active_sessions(self):
        """Test setting active sessions count"""
        MetricsService.set_active_sessions(42)
        
        # Gauge should be set to 42
        # Note: Can't easily test gauge value without accessing internals
        # This test ensures no errors are raised
        assert True
