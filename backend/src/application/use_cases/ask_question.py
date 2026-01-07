from src.domain.qa import Question, Answer
from src.domain.learning_session import SessionStatus
from src.infrastructure.database.session_repository import SessionRepository
from src.infrastructure.database.qa_repository import QuestionRepository, AnswerRepository
from src.infrastructure.cache.redis_service import CacheService
from src.infrastructure.llm.openai_service import LLMService
import hashlib

class AskQuestionUseCase:
    def __init__(
        self,
        session_repository: SessionRepository,
        question_repository: QuestionRepository,
        answer_repository: AnswerRepository,
        cache_service: CacheService,
        llm_service: LLMService
    ):
        self.session_repository = session_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository
        self.cache_service = cache_service
        self.llm_service = llm_service
    
    def execute(self, session_id: str, user_id: str, content: str) -> dict:
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
        
        if session.user_id != user_id:
            raise ValueError("Unauthorized")
        
        if self.cache_service.is_locked(session_id):
            raise ValueError("Session is processing another question")
        
        question_hash = hashlib.sha256(content.lower().strip().encode()).hexdigest()
        cached_answer = self.cache_service.get_cached_answer(question_hash)
        
        if cached_answer:
            question = Question(session_id=session_id, content=content)
            created_question = self.question_repository.create(question)
            
            answer = Answer(
                question_id=created_question.id,
                content=cached_answer["content"],
                explanation=cached_answer["explanation"],
                edge_cases=cached_answer["edge_cases"]
            )
            created_answer = self.answer_repository.create(answer)
            
            return {
                "question_id": created_question.id,
                "answer_id": created_answer.id,
                "content": created_answer.content,
                "explanation": created_answer.explanation,
                "edge_cases": created_answer.edge_cases
            }
        
        if not self.cache_service.acquire_lock(session_id, ttl=180):
            raise ValueError("Failed to acquire lock")
        
        try:
            self.session_repository.update_status(session_id, SessionStatus.PROCESSING)
            
            question = Question(session_id=session_id, content=content)
            created_question = self.question_repository.create(question)
            
            llm_response = self.llm_service.generate_socratic_answer(content)
            
            answer = Answer(
                question_id=created_question.id,
                content=llm_response["content"],
                explanation=llm_response["explanation"],
                edge_cases=llm_response["edge_cases"]
            )
            created_answer = self.answer_repository.create(answer)
            
            self.cache_service.cache_answer(question_hash, {
                "content": created_answer.content,
                "explanation": created_answer.explanation,
                "edge_cases": created_answer.edge_cases
            })
            
            self.session_repository.update_status(session_id, SessionStatus.ACTIVE)
            
            return {
                "question_id": created_question.id,
                "answer_id": created_answer.id,
                "content": created_answer.content,
                "explanation": created_answer.explanation,
                "edge_cases": created_answer.edge_cases
            }
        
        finally:
            self.cache_service.release_lock(session_id)