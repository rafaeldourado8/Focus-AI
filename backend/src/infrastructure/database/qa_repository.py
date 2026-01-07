from typing import Optional
from sqlalchemy.orm import Session
from src.domain.qa import Question, Answer
from src.infrastructure.database.models import QuestionModel, AnswerModel

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, question: Question) -> Question:
        db_question = QuestionModel(
            session_id=question.session_id,
            content=question.content
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return Question(
            id=db_question.id,
            session_id=db_question.session_id,
            content=db_question.content,
            created_at=db_question.created_at
        )
    
    def get_by_id(self, question_id: str) -> Optional[Question]:
        db_question = self.db.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).first()
        if not db_question:
            return None
        return Question(
            id=db_question.id,
            session_id=db_question.session_id,
            content=db_question.content,
            created_at=db_question.created_at
        )

class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, answer: Answer) -> Answer:
        db_answer = AnswerModel(
            question_id=answer.question_id,
            content=answer.content,
            explanation=answer.explanation,
            edge_cases=answer.edge_cases
        )
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return Answer(
            id=db_answer.id,
            question_id=db_answer.question_id,
            content=db_answer.content,
            explanation=db_answer.explanation,
            edge_cases=db_answer.edge_cases,
            created_at=db_answer.created_at
        )
    
    def get_by_question_id(self, question_id: str) -> Optional[Answer]:
        db_answer = self.db.query(AnswerModel).filter(
            AnswerModel.question_id == question_id
        ).first()
        if not db_answer:
            return None
        return Answer(
            id=db_answer.id,
            question_id=db_answer.question_id,
            content=db_answer.content,
            explanation=db_answer.explanation,
            edge_cases=db_answer.edge_cases,
            created_at=db_answer.created_at
        )