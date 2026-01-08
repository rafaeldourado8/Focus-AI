from src.domain.qa import Question, Answer
from src.domain.learning_session import SessionStatus
from src.infrastructure.database.session_repository import SessionRepository
from src.infrastructure.database.qa_repository import QuestionRepository, AnswerRepository
from src.infrastructure.cache.redis_service import CacheService
from src.infrastructure.llm.chain_validator_service import ChainValidatorService
import hashlib

class AskQuestionUseCase:
    def __init__(
        self,
        session_repository: SessionRepository,
        question_repository: QuestionRepository,
        answer_repository: AnswerRepository,
        cache_service: CacheService,
        llm_service: ChainValidatorService
    ):
        self.session_repository = session_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository
        self.cache_service = cache_service
        self.llm_service = llm_service
    
    def execute(self, session_id: str, user_id: str, content: str, debug_mode: bool = False, language: str = "pt-BR") -> dict:
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
                explanation="",
                edge_cases=""
            )
            created_answer = self.answer_repository.create(answer)
            
            return {
                "content": created_answer.content,
                "answer_id": created_answer.id,
                "model": cached_answer.get("model", "cached"),
                "used_senior": cached_answer.get("used_senior", False),
                "thinking_process": []
            }
        
        if not self.cache_service.acquire_lock(session_id, ttl=180):
            raise ValueError("Failed to acquire lock")
        
        try:
            self.session_repository.update_status(session_id, SessionStatus.PROCESSING)
            
            question = Question(session_id=session_id, content=content)
            created_question = self.question_repository.create(question)
            
            llm_response = self.llm_service.generate_answer(content, debug_mode=debug_mode, language=language)
            
            answer = Answer(
                question_id=created_question.id,
                content=llm_response["content"],
                explanation="",
                edge_cases=""
            )
            created_answer = self.answer_repository.create(answer)
            
            self.cache_service.cache_answer(question_hash, {
                "content": created_answer.content,
                "model": llm_response["model"],
                "used_senior": llm_response["used_senior"]
            })
            
            # Gerar processo de pensamento
            thinking_process = self._generate_thinking_process(content, llm_response)
            
            self.session_repository.update_status(session_id, SessionStatus.ACTIVE)
            
            return {
                "content": created_answer.content,
                "answer_id": created_answer.id,
                "model": llm_response["model"],
                "used_senior": llm_response["used_senior"],
                "thinking_process": thinking_process
            }
        
        finally:
            self.cache_service.release_lock(session_id)
    
    def _generate_thinking_process(self, question: str, llm_response: dict) -> list:
        """Gera processo de pensamento estilo Gemini"""
        steps = []
        
        # Análise da pergunta
        steps.append({
            "step": "Analisando pergunta",
            "description": f"Identificando contexto e requisitos técnicos",
            "status": "completed"
        })
        
        # Escolha do modelo
        model_name = "Cerberus Lite" if "lite" in llm_response.get("model", "").lower() else "Cerberus Pro"
        steps.append({
            "step": "Selecionando modelo",
            "description": f"Usando {model_name} para esta resposta",
            "status": "completed"
        })
        
        # Busca de contexto (se RAG estiver ativo)
        if llm_response.get("used_rag", False):
            steps.append({
                "step": "Buscando contexto",
                "description": "Consultando base de conhecimento técnico",
                "status": "completed"
            })
        
        # Geração da resposta
        steps.append({
            "step": "Gerando resposta",
            "description": "Processando informações e criando solução",
            "status": "completed"
        })
        
        # Validação (se Senior foi usado)
        if llm_response.get("used_senior", False):
            steps.append({
                "step": "Validando qualidade",
                "description": "Revisão técnica com modelo avançado",
                "status": "completed"
            })
        
        return steps