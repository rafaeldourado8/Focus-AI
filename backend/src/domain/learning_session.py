from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class SessionStatus(str, Enum):
    ACTIVE = "active"
    PROCESSING = "processing"
    COMPLETED = "completed"

class LearningSession(BaseModel):
    id: Optional[str] = None
    user_id: str
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True