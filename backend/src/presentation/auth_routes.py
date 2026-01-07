from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.user_repository import UserRepository
from src.infrastructure.auth.auth_service import AuthService
from src.config import get_settings
from src.domain.user import User
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()
settings = get_settings()

class GoogleLoginRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user_id = AuthService.verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user_repo = UserRepository(db)
    if not user_repo.get_by_id(user_id):
        raise HTTPException(status_code=401, detail="Utilizador não encontrado no banco")
    return user_id

@router.post("/google", response_model=TokenResponse)
async def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        # Corrigido: margem de 15 segundos para dessincronização de relógio
        idinfo = id_token.verify_oauth2_token(
            request.token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=15
        )

        email = idinfo.get('email')
        user_repo = UserRepository(db)
        user = user_repo.get_by_email(email)
        
        if not user:
            user_entity = User(
                email=email,
                password_hash="google_oauth",
                is_active=True
            )
            user = user_repo.create(user_entity)
        
        token = AuthService.create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token)
        
    except Exception as e:
        logger.error(f"Google login fail: {e}")
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me")
async def get_current_user(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    return {"user_id": user.id, "email": user.email}