from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.presentation.auth_routes import verify_token
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.session_repository import SessionRepository
from src.infrastructure.database.qa_repository import QuestionRepository, AnswerRepository
from src.infrastructure.cache.redis_service import CacheService
from src.infrastructure.llm.chain_validator_service import ChainValidatorService
from src.application.use_cases.create_session import CreateSessionUseCase
from src.application.use_cases.ask_question import AskQuestionUseCase

router = APIRouter()

from pydantic import BaseModel

class QuestionRequest(BaseModel):
    content: str
    debug_mode: bool = False

class SessionResponse(BaseModel):
    session_id: str
    status: str

class AnswerResponse(BaseModel):
    content: str
    model: str = "gemini"
    used_senior: bool = False

@router.post("/", response_model=SessionResponse)
async def create_session(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    session_repo = SessionRepository(db)
    use_case = CreateSessionUseCase(session_repo)
    result = use_case.execute(user_id)
    return SessionResponse(session_id=result["session_id"], status=result["status"])

@router.get("/")
async def list_sessions(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Lista todas as sessões do usuário"""
    session_repo = SessionRepository(db)
    question_repo = QuestionRepository(db)
    
    sessions = session_repo.get_by_user(user_id)
    
    result = []
    for session in sessions:
        # Busca primeira pergunta para usar como título
        questions = question_repo.get_by_session(session.id)
        title = questions[0].content[:50] + "..." if questions else "Nova conversa"
        
        result.append({
            "id": session.id,
            "title": title,
            "status": session.status.value,
            "created_at": session.created_at.isoformat(),
            "message_count": len(questions)
        })
    
    return {"sessions": result}

@router.post("/{session_id}/questions", response_model=AnswerResponse)
async def ask_question(
    session_id: str, 
    request: QuestionRequest,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    try:
        session_repo = SessionRepository(db)
        question_repo = QuestionRepository(db)
        answer_repo = AnswerRepository(db)
        cache_service = CacheService()
        llm_service = ChainValidatorService()
        
        use_case = AskQuestionUseCase(
            session_repo,
            question_repo,
            answer_repo,
            cache_service,
            llm_service
        )
        
        result = use_case.execute(session_id, user_id, request.content, request.debug_mode)
        
        return AnswerResponse(
            content=result["content"],
            model=result.get("model", "gemini"),
            used_senior=result.get("used_senior", False)
        )
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        elif "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        elif "processing" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/{session_id}/history")
async def get_session_history(
    session_id: str,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Retorna histórico completo de uma sessão"""
    session_repo = SessionRepository(db)
    question_repo = QuestionRepository(db)
    answer_repo = AnswerRepository(db)
    
    # Valida sessão
    session = session_repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Busca perguntas e respostas
    questions = question_repo.get_by_session(session_id)
    
    history = []
    for question in questions:
        answer = answer_repo.get_by_question_id(question.id)
        history.append({
            "question": {
                "id": question.id,
                "content": question.content,
                "created_at": question.created_at.isoformat()
            },
            "answer": {
                "id": answer.id,
                "content": answer.content,
                "created_at": answer.created_at.isoformat()
            } if answer else None
        })
    
    return {
        "session_id": session_id,
        "history": history
    }

@router.get("/{session_id}")
async def get_session(
    session_id: str, 
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    session = session_repo.get_by_id(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {
        "session_id": session.id,
        "status": session.status.value,
        "created_at": session.created_at.isoformat()
    }