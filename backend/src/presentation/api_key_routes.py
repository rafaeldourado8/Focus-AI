"""
API Keys Management Routes

CRUD operations for API keys
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.api_key_repository import APIKeyRepository
from src.infrastructure.auth.auth_service import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()


# Request/Response models
class CreateAPIKeyRequest(BaseModel):
    name: str
    plan: str = "free"


class APIKeyResponse(BaseModel):
    key: str
    name: str
    plan: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    usage_count: int
    rate_limit: int
    daily_limit: Optional[int]


class APIKeyListResponse(BaseModel):
    keys: List[APIKeyResponse]


@router.post("/", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateAPIKeyRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new API key"""
    repo = APIKeyRepository(db)
    api_key = repo.create(
        user_id=current_user["user_id"],
        name=request.name,
        plan=request.plan
    )
    
    return APIKeyResponse(
        key=api_key.key,
        name=api_key.name,
        plan=api_key.plan,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
        last_used_at=api_key.last_used_at,
        usage_count=api_key.usage_count,
        rate_limit=api_key.get_rate_limit(),
        daily_limit=api_key.get_daily_limit()
    )


@router.get("/", response_model=APIKeyListResponse)
async def list_api_keys(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all API keys for current user"""
    repo = APIKeyRepository(db)
    keys = repo.get_by_user(current_user["user_id"])
    
    return APIKeyListResponse(
        keys=[
            APIKeyResponse(
                key=k.key,
                name=k.name,
                plan=k.plan,
                is_active=k.is_active,
                created_at=k.created_at,
                expires_at=k.expires_at,
                last_used_at=k.last_used_at,
                usage_count=k.usage_count,
                rate_limit=k.get_rate_limit(),
                daily_limit=k.get_daily_limit()
            )
            for k in keys
        ]
    )


@router.post("/{key}/rotate", response_model=APIKeyResponse)
async def rotate_api_key(
    key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rotate API key (create new, deactivate old)"""
    repo = APIKeyRepository(db)
    
    # Verify ownership
    existing = repo.get_by_key(key)
    if not existing or existing.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    new_key = repo.rotate(key)
    
    return APIKeyResponse(
        key=new_key.key,
        name=new_key.name,
        plan=new_key.plan,
        is_active=new_key.is_active,
        created_at=new_key.created_at,
        expires_at=new_key.expires_at,
        last_used_at=new_key.last_used_at,
        usage_count=new_key.usage_count,
        rate_limit=new_key.get_rate_limit(),
        daily_limit=new_key.get_daily_limit()
    )


@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_api_key(
    key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate API key"""
    repo = APIKeyRepository(db)
    
    # Verify ownership
    existing = repo.get_by_key(key)
    if not existing or existing.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    repo.deactivate(key)
    return None


@router.get("/{key}/usage")
async def get_api_key_usage(
    key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get usage statistics for API key"""
    repo = APIKeyRepository(db)
    
    api_key = repo.get_by_key(key)
    if not api_key or api_key.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return {
        "key": api_key.key[:8] + "...",
        "name": api_key.name,
        "plan": api_key.plan,
        "total_requests": api_key.usage_count,
        "last_used_at": api_key.last_used_at,
        "rate_limit": api_key.get_rate_limit(),
        "daily_limit": api_key.get_daily_limit()
    }
