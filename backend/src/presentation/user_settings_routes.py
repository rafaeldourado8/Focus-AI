from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.presentation.auth_routes import verify_token
from src.infrastructure.database.connection import get_db

router = APIRouter()

class UserSettingsUpdate(BaseModel):
    name: str = None
    debug_mode: bool = False
    language: str = "pt-BR"
    notifications: bool = True

@router.get("/me")
async def get_user_settings(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Retorna configurações do usuário"""
    from src.infrastructure.database.models import UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "email": user.email,
        "name": user.name or "",
        "settings": {
            "debugMode": user.debug_mode,
            "language": user.language,
            "notifications": user.notifications
        }
    }

@router.put("/me")
async def update_user_settings(
    settings: UserSettingsUpdate,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Atualiza configurações do usuário"""
    from src.infrastructure.database.models import UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if settings.name is not None:
        user.name = settings.name
    user.debug_mode = settings.debug_mode
    user.language = settings.language
    user.notifications = settings.notifications
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Configurações atualizadas com sucesso",
        "settings": {
            "debugMode": user.debug_mode,
            "language": user.language,
            "notifications": user.notifications
        }
    }
