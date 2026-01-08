"""
Public API v1 Routes

OpenAI-compatible endpoints for external integrations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from src.infrastructure.api_gateway.middleware import APIGatewayMiddleware
from src.infrastructure.database.api_key_repository import APIKeyRepository
from src.infrastructure.database.connection import get_db
from src.infrastructure.orchestrator.model_router import ModelRouter
from src.infrastructure.llm.chain_validator_service import ChainValidatorService
from src.infrastructure.monitoring.metrics_service import MetricsService, RequestTimer
from src.infrastructure.identity import MODEL_JUNIOR, MODEL_SENIOR, MODEL_DEBUG, get_public_model_name
from sqlalchemy.orm import Session
import time

router = APIRouter()


# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "cerberus-pro"
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = False
    debug_mode: bool = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]
    metadata: Optional[Dict[str, Any]] = None


class CodeAnalyzeRequest(BaseModel):
    code: str
    language: str
    checks: List[str] = ["security", "performance", "style"]


class CodeDebugRequest(BaseModel):
    error: str
    code: str
    language: str
    context: Optional[str] = None


class CodeRefactorRequest(BaseModel):
    code: str
    language: str
    goals: List[str] = ["readability", "maintainability"]


class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    max_tokens: int
    cost_per_1k_tokens: float
    available_in: List[str]


# Dependency for API authentication
async def get_api_key(db: Session = Depends(get_db)):
    """Authenticate and validate API key"""
    from fastapi import Request
    request = Request(scope={"type": "http"})
    
    repo = APIKeyRepository(db)
    middleware = APIGatewayMiddleware(repo)
    
    api_key = await middleware.authenticate(request)
    rate_info = middleware.check_rate_limit(api_key)
    
    # Increment usage
    repo.increment_usage(api_key.key)
    
    return {"api_key": api_key, "rate_info": rate_info}


@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest,
    auth = Depends(get_api_key)
):
    """
    OpenAI-compatible chat completions endpoint
    
    Create a chat completion using Cerberus AI models
    """
    api_key = auth["api_key"]
    
    # Route to appropriate model
    router_service = ModelRouter()
    last_message = request.messages[-1].content if request.messages else ""
    
    route_info = router_service.route(
        question=last_message,
        debug_mode=request.debug_mode,
        force_model=request.model if request.model != "cerberus-pro" else None
    )
    
    # Track metrics
    with RequestTimer(route_info["model"] or "cache", "chat") as timer:
        # Check cache
        if route_info["use_cache"]:
            MetricsService.track_cache_hit()
            # Return cached response (simplified)
            return ChatCompletionResponse(
                id=f"chatcmpl-{int(time.time())}",
                created=int(time.time()),
                model=get_public_model_name(MODEL_JUNIOR),
                choices=[{
                    "index": 0,
                    "message": {"role": "assistant", "content": "Cached response"},
                    "finish_reason": "stop"
                }],
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            )
        
        MetricsService.track_cache_miss()
        
        # Generate response
        llm_service = ChainValidatorService()
        
        # Convert messages to conversation history
        history = [
            {"role": msg.role, "parts": [msg.content]}
            for msg in request.messages[:-1]
        ]
        
        result = llm_service.generate_answer(
            question=last_message,
            conversation_history=history if history else None,
            debug_mode=request.debug_mode
        )
        
        # Track cost
        MetricsService.track_cost(route_info["estimated_cost"])
        MetricsService.track_model_usage(route_info["model"])
    
    return ChatCompletionResponse(
        id=f"chatcmpl-{int(time.time())}",
        created=int(time.time()),
        model=result["model"],
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": result["content"]},
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": len(last_message.split()),
            "completion_tokens": len(result["content"].split()),
            "total_tokens": len(last_message.split()) + len(result["content"].split())
        },
        metadata={
            "cache_hit": route_info["use_cache"],
            "latency_ms": int(timer.duration * 1000) if timer.duration else 0
        }
    )


@router.post("/code/analyze")
async def code_analyze(
    request: CodeAnalyzeRequest,
    auth = Depends(get_api_key)
):
    """Analyze code for issues"""
    prompt = f"""Analyze this {request.language} code for {', '.join(request.checks)}:

```{request.language}
{request.code}
```

Provide a JSON response with issues found."""
    
    llm_service = ChainValidatorService()
    result = llm_service.generate_answer(prompt, debug_mode=False)
    
    return {"analysis": result["content"], "model": result["model"]}


@router.post("/code/debug")
async def code_debug(
    request: CodeDebugRequest,
    auth = Depends(get_api_key)
):
    """Debug code with error"""
    prompt = f"""Debug this {request.language} code error:

Error: {request.error}

Code:
```{request.language}
{request.code}
```

Context: {request.context or 'None'}

Provide root cause and solutions."""
    
    llm_service = ChainValidatorService()
    result = llm_service.generate_answer(prompt, debug_mode=True)
    
    return {"debug_info": result["content"], "model": result["model"]}


@router.post("/code/refactor")
async def code_refactor(
    request: CodeRefactorRequest,
    auth = Depends(get_api_key)
):
    """Refactor code"""
    prompt = f"""Refactor this {request.language} code for {', '.join(request.goals)}:

```{request.language}
{request.code}
```

Provide refactored code and explanation."""
    
    llm_service = ChainValidatorService()
    result = llm_service.generate_answer(prompt, debug_mode=False)
    
    return {"refactored": result["content"], "model": result["model"]}


@router.get("/models")
async def list_models(auth = Depends(get_api_key)):
    """List available models"""
    return {
        "models": [
            ModelInfo(
                id=MODEL_JUNIOR,
                name="Cerberus Lite",
                description="Fast responses, general coding",
                max_tokens=2048,
                cost_per_1k_tokens=0.0001,
                available_in=["free", "pro", "enterprise"]
            ),
            ModelInfo(
                id=MODEL_SENIOR,
                name="Cerberus Pro",
                description="Advanced debugging and architecture",
                max_tokens=8192,
                cost_per_1k_tokens=0.001,
                available_in=["pro", "enterprise"]
            ),
            ModelInfo(
                id=MODEL_DEBUG,
                name="Cerberus Debug",
                description="Deep technical analysis",
                max_tokens=8192,
                cost_per_1k_tokens=0.001,
                available_in=["pro", "enterprise"]
            )
        ]
    }


@router.get("/usage")
async def get_usage(auth = Depends(get_api_key)):
    """Get usage statistics"""
    api_key = auth["api_key"]
    
    return {
        "key": api_key.key[:8] + "...",
        "plan": api_key.plan,
        "total_requests": api_key.usage_count,
        "rate_limit": api_key.get_rate_limit(),
        "daily_limit": api_key.get_daily_limit()
    }
