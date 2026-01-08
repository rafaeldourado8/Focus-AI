"""Conversation Logger for Training Data Collection"""
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from src.domain.training_example import TrainingExample


class ConversationLogger:
    """Logs conversations for training data collection"""
    
    def __init__(self, log_dir: str = "data/training_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_conversation(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_message: str,
        context: Optional[str] = None,
        language: Optional[str] = None,
        framework: Optional[str] = None,
        complexity: int = 5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log a conversation exchange (anonymized)"""
        example_id = self._generate_id(user_id, session_id, user_message)
        anonymized_user_id = self._anonymize(user_id)
        
        example = TrainingExample(
            id=example_id,
            user_message=self._anonymize_pii(user_message),
            assistant_message=self._anonymize_pii(assistant_message),
            context=context,
            feedback_score=None,
            language=language,
            framework=framework,
            complexity=complexity,
            created_at=datetime.utcnow(),
            metadata={
                "anonymized_user_id": anonymized_user_id,
                "session_id": session_id,
                **(metadata or {})
            }
        )
        
        self._write_log(example)
        return example_id
    
    def add_feedback(self, example_id: str, score: int):
        """Add user feedback to logged conversation"""
        feedback_file = self.log_dir / "feedback.jsonl"
        with open(feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "example_id": example_id,
                "score": score,
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")
    
    def _write_log(self, example: TrainingExample):
        """Write example to JSONL file"""
        date_str = example.created_at.strftime("%Y-%m-%d")
        log_file = self.log_dir / f"conversations_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "id": example.id,
                "user_message": example.user_message,
                "assistant_message": example.assistant_message,
                "context": example.context,
                "language": example.language,
                "framework": example.framework,
                "complexity": example.complexity,
                "created_at": example.created_at.isoformat(),
                "metadata": example.metadata
            }) + "\n")
    
    def _generate_id(self, user_id: str, session_id: str, message: str) -> str:
        """Generate unique example ID"""
        data = f"{user_id}:{session_id}:{message}:{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _anonymize(self, user_id: str) -> str:
        """Anonymize user ID"""
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]
    
    def _anonymize_pii(self, text: str) -> str:
        """Remove PII from text (basic implementation)"""
        # TODO: Implement proper PII detection/removal
        return text
