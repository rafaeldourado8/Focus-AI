import pytest
from src.domain.qa import Question, Answer

def test_question_creation():
    question = Question(session_id="session123", content="What is DDD?")
    assert question.session_id == "session123"
    assert question.content == "What is DDD?"
    assert question.id is None

def test_answer_creation():
    answer = Answer(
        question_id="q123",
        content="DDD is Domain-Driven Design",
        explanation="It's a software design approach",
        edge_cases="Consider bounded contexts"
    )
    assert answer.question_id == "q123"
    assert answer.content == "DDD is Domain-Driven Design"
    assert answer.explanation == "It's a software design approach"
    assert answer.edge_cases == "Consider bounded contexts"

def test_answer_without_edge_cases():
    answer = Answer(
        question_id="q123",
        content="Content",
        explanation="Explanation"
    )
    assert answer.edge_cases is None