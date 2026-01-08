"""
Prometheus Metrics Service

Exposes application metrics for monitoring:
- Request latency
- Cache hit rate
- Model usage
- Error rate
- Cost tracking
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import logging

logger = logging.getLogger(__name__)


# Request metrics
requests_total = Counter(
    'cerberus_requests_total',
    'Total number of requests',
    ['model', 'status']
)

request_duration = Histogram(
    'cerberus_request_duration_seconds',
    'Request duration in seconds',
    ['model', 'endpoint']
)

# Cache metrics
cache_hits = Counter(
    'cerberus_cache_hits_total',
    'Total cache hits'
)

cache_misses = Counter(
    'cerberus_cache_misses_total',
    'Total cache misses'
)

# Model usage
model_usage = Counter(
    'cerberus_model_usage_total',
    'Model usage count',
    ['model']
)

# Cost tracking
total_cost = Counter(
    'cerberus_total_cost_usd',
    'Total cost in USD'
)

# Error tracking
errors_total = Counter(
    'cerberus_errors_total',
    'Total errors',
    ['error_type']
)

# Active sessions
active_sessions = Gauge(
    'cerberus_active_sessions',
    'Number of active sessions'
)


class MetricsService:
    """Service for tracking and exposing metrics"""
    
    @staticmethod
    def track_request(model: str, status: str, duration: float, endpoint: str = "chat"):
        """Track request metrics"""
        requests_total.labels(model=model, status=status).inc()
        request_duration.labels(model=model, endpoint=endpoint).observe(duration)
        logger.debug(f"Tracked request: model={model}, status={status}, duration={duration:.3f}s")
    
    @staticmethod
    def track_cache_hit():
        """Track cache hit"""
        cache_hits.inc()
    
    @staticmethod
    def track_cache_miss():
        """Track cache miss"""
        cache_misses.inc()
    
    @staticmethod
    def track_model_usage(model: str):
        """Track model usage"""
        model_usage.labels(model=model).inc()
    
    @staticmethod
    def track_cost(cost: float):
        """Track cost in USD"""
        total_cost.inc(cost)
    
    @staticmethod
    def track_error(error_type: str):
        """Track error"""
        errors_total.labels(error_type=error_type).inc()
        logger.warning(f"Error tracked: {error_type}")
    
    @staticmethod
    def set_active_sessions(count: int):
        """Set active sessions count"""
        active_sessions.set(count)
    
    @staticmethod
    def get_metrics() -> bytes:
        """Get Prometheus metrics in text format"""
        return generate_latest()
    
    @staticmethod
    def get_content_type() -> str:
        """Get Prometheus content type"""
        return CONTENT_TYPE_LATEST


class RequestTimer:
    """Context manager for timing requests"""
    
    def __init__(self, model: str, endpoint: str = "chat"):
        self.model = model
        self.endpoint = endpoint
        self.start_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        status = "error" if exc_type else "success"
        MetricsService.track_request(self.model, status, self.duration, self.endpoint)
        return False
