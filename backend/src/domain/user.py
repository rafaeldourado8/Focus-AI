from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password_hash: str
    created_at: Optional[datetime] = None
    career_stage: Optional[str] = None
    is_active: bool = False  
    activation_code: Optional[str] = None
    
    class Config:
        from_attributes = True