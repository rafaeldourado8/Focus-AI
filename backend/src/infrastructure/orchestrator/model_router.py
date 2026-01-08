"""
Model Router - Intelligent LLM routing

Routes requests to appropriate model based on:
- Complexity
- Debug mode
- Cache availability
- Cost optimization
"""

import logging
from typing import Dict, Any, Optional
from src.infrastructure.identity import MODEL_JUNIOR, MODEL_SENIOR, MODEL_DEBUG
from src.infrastructure.cache.redis_service import CacheService

logger = logging.getLogger(__name__)


class ModelRouter:
    """Intelligent model routing with cost optimization"""
    
    # Complexity thresholds
    COMPLEXITY_LOW = 3
    COMPLEXITY_HIGH = 8
    
    # Cost per 1K tokens (USD)
    COST_JUNIOR = 0.0001
    COST_SENIOR = 0.001
    
    def __init__(self, cache_service: Optional[CacheService] = None):
        self.cache = cache_service or CacheService()
        self.metrics = {
            "total_requests": 0,
            "junior_used": 0,
            "senior_used": 0,
            "cache_hits": 0,
            "total_cost": 0.0
        }
    
    def route(self, question: str, debug_mode: bool = False, 
              force_model: Optional[str] = None) -> Dict[str, Any]:
        """
        Route request to appropriate model
        
        Returns:
            {
                "model": str,
                "use_cache": bool,
                "reason": str,
                "estimated_cost": float
            }
        """
        self.metrics["total_requests"] += 1
        
        # Force specific model
        if force_model:
            return self._route_forced(force_model)
        
        # Debug mode always uses senior
        if debug_mode:
            return self._route_debug()
        
        # Check cache first
        cached = self.cache.get_cached_answer(question)
        if cached:
            self.metrics["cache_hits"] += 1
            return {
                "model": None,
                "use_cache": True,
                "reason": "cache_hit",
                "estimated_cost": 0.0
            }
        
        # Route by complexity
        complexity = self._calculate_complexity(question)
        
        if complexity >= self.COMPLEXITY_HIGH:
            return self._route_senior(complexity)
        else:
            return self._route_junior(complexity)
    
    def _calculate_complexity(self, question: str) -> int:
        """
        Calculate question complexity (0-10)
        
        Factors:
        - Length
        - Technical keywords
        - Code blocks
        - Multiple questions
        """
        score = 0
        lower_q = question.lower()
        
        # Length factor
        if len(question) > 500:
            score += 2
        elif len(question) > 200:
            score += 1
        
        # Technical keywords
        technical_keywords = [
            "architecture", "scalability", "performance", "optimization",
            "design pattern", "refactor", "debug", "error", "exception",
            "async", "concurrent", "thread", "race condition", "deadlock"
        ]
        score += sum(1 for kw in technical_keywords if kw in lower_q)
        
        # Code blocks
        if "```" in question:
            score += 2
        
        # Multiple questions
        if question.count("?") > 1:
            score += 1
        
        return min(score, 10)
    
    def _route_junior(self, complexity: int) -> Dict[str, Any]:
        """Route to junior model"""
        self.metrics["junior_used"] += 1
        cost = self._estimate_cost(MODEL_JUNIOR)
        self.metrics["total_cost"] += cost
        
        logger.info(f"Routing to JUNIOR (complexity: {complexity})")
        
        return {
            "model": MODEL_JUNIOR,
            "use_cache": False,
            "reason": f"low_complexity_{complexity}",
            "estimated_cost": cost
        }
    
    def _route_senior(self, complexity: int) -> Dict[str, Any]:
        """Route to senior model"""
        self.metrics["senior_used"] += 1
        cost = self._estimate_cost(MODEL_SENIOR)
        self.metrics["total_cost"] += cost
        
        logger.info(f"Routing to SENIOR (complexity: {complexity})")
        
        return {
            "model": MODEL_SENIOR,
            "use_cache": False,
            "reason": f"high_complexity_{complexity}",
            "estimated_cost": cost
        }
    
    def _route_debug(self) -> Dict[str, Any]:
        """Route to debug model"""
        self.metrics["senior_used"] += 1
        cost = self._estimate_cost(MODEL_DEBUG)
        self.metrics["total_cost"] += cost
        
        logger.info("Routing to DEBUG mode")
        
        return {
            "model": MODEL_DEBUG,
            "use_cache": False,
            "reason": "debug_mode",
            "estimated_cost": cost
        }
    
    def _route_forced(self, model: str) -> Dict[str, Any]:
        """Route to forced model"""
        cost = self._estimate_cost(model)
        self.metrics["total_cost"] += cost
        
        if model == MODEL_JUNIOR:
            self.metrics["junior_used"] += 1
        else:
            self.metrics["senior_used"] += 1
        
        logger.info(f"Routing to FORCED model: {model}")
        
        return {
            "model": model,
            "use_cache": False,
            "reason": "forced",
            "estimated_cost": cost
        }
    
    def _estimate_cost(self, model: str, tokens: int = 1000) -> float:
        """Estimate cost for model (default 1K tokens)"""
        if model == MODEL_JUNIOR:
            return self.COST_JUNIOR * (tokens / 1000)
        else:
            return self.COST_SENIOR * (tokens / 1000)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get routing metrics"""
        total = self.metrics["total_requests"]
        
        return {
            **self.metrics,
            "junior_percentage": round((self.metrics["junior_used"] / total * 100) if total > 0 else 0, 2),
            "senior_percentage": round((self.metrics["senior_used"] / total * 100) if total > 0 else 0, 2),
            "cache_hit_rate": round((self.metrics["cache_hits"] / total * 100) if total > 0 else 0, 2),
            "avg_cost_per_request": round(self.metrics["total_cost"] / total if total > 0 else 0, 6)
        }
    
    def fallback(self, failed_model: str, question: str) -> Dict[str, Any]:
        """
        Fallback to alternative model on failure
        
        Fallback chain: Senior -> Junior -> Error
        """
        logger.warning(f"Model {failed_model} failed, attempting fallback")
        
        if failed_model == MODEL_SENIOR or failed_model == MODEL_DEBUG:
            logger.info("Falling back to JUNIOR")
            return self._route_junior(0)
        
        # No more fallbacks
        logger.error("All models failed")
        return {
            "model": None,
            "use_cache": False,
            "reason": "all_models_failed",
            "estimated_cost": 0.0
        }
