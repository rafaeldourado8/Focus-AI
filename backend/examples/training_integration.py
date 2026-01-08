"""Example: Integrating Training Data Collection in Production"""

# ============================================
# 1. Backend Integration (process_question.py)
# ============================================

from src.infrastructure.training.conversation_logger import ConversationLogger
from src.infrastructure.training.feedback_collector import FeedbackCollector

# Initialize logger (singleton pattern recommended)
conversation_logger = ConversationLogger(log_dir="data/training_logs")

async def process_question_with_logging(
    user_id: str,
    session_id: str,
    question: str,
    context: str
) -> dict:
    """Process question and log for training"""
    
    # Generate AI response (existing logic)
    response = await generate_response(question, context)
    
    # Log conversation for training
    example_id = conversation_logger.log_conversation(
        user_id=user_id,
        session_id=session_id,
        user_message=question,
        assistant_message=response["content"],
        context=context,
        language=detect_language(question),
        framework=detect_framework(question),
        complexity=response.get("complexity", 5),
        metadata={
            "model": response.get("model"),
            "tokens": response.get("tokens"),
            "latency_ms": response.get("latency_ms")
        }
    )
    
    # Return response with example_id for feedback
    return {
        **response,
        "example_id": example_id
    }


# ============================================
# 2. Feedback API Endpoint (public_routes.py)
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/v1", tags=["feedback"])

class FeedbackRequest(BaseModel):
    example_id: str
    score: int  # 1-5
    comment: str | None = None

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback on AI response"""
    try:
        collector = FeedbackCollector(conversation_logger)
        collector.submit_feedback(
            example_id=request.example_id,
            score=request.score,
            comment=request.comment
        )
        return {"status": "success", "message": "Feedback recorded"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# 3. Language/Framework Detection Helpers
# ============================================

def detect_language(text: str) -> str | None:
    """Detect programming language from text"""
    keywords = {
        "python": ["def ", "import ", "class ", "async ", "await "],
        "javascript": ["function ", "const ", "let ", "var ", "=>"],
        "typescript": ["interface ", "type ", ": string", ": number"],
        "java": ["public class", "private ", "void ", "String "],
        "go": ["func ", "package ", "import "],
        "rust": ["fn ", "let mut", "impl ", "trait "],
    }
    
    text_lower = text.lower()
    for lang, patterns in keywords.items():
        if any(pattern.lower() in text_lower for pattern in patterns):
            return lang
    
    return None


def detect_framework(text: str) -> str | None:
    """Detect framework from text"""
    frameworks = {
        "fastapi": ["fastapi", "@app.get", "@app.post", "APIRouter"],
        "django": ["django", "models.Model", "views.py", "urls.py"],
        "flask": ["flask", "@app.route", "Flask(__name__)"],
        "react": ["react", "useState", "useEffect", "jsx"],
        "vue": ["vue", "v-if", "v-for", "computed"],
        "express": ["express", "app.listen", "req.body", "res.json"],
    }
    
    text_lower = text.lower()
    for framework, patterns in frameworks.items():
        if any(pattern.lower() in text_lower for pattern in patterns):
            return framework
    
    return None
