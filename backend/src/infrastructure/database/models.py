from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    PROCESSING = "processing"
    COMPLETED = "completed"

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    career_stage = Column(String, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    activation_code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    debug_mode = Column(Boolean, default=False)
    language = Column(String, default="pt-BR")
    notifications = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("LearningSessionModel", back_populates="user")

class LearningSessionModel(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserModel", back_populates="sessions")
    questions = relationship("QuestionModel", back_populates="session")

class QuestionModel(Base):
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("learning_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("LearningSessionModel", back_populates="questions")
    answer = relationship("AnswerModel", back_populates="question", uselist=False)

class AnswerModel(Base):
    __tablename__ = "answers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    content = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    edge_cases = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    question = relationship("QuestionModel", back_populates="answer")