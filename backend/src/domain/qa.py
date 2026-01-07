from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Question(BaseModel):
    id: Optional[str] = None
    session_id: str
    content: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Answer(BaseModel):
    id: Optional[str] = None
    question_id: str
    content: str
    explanation: str
    edge_cases: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True