"""Feedback Collector for Training Data Quality"""
from typing import Optional
from datetime import datetime

from src.infrastructure.training.conversation_logger import ConversationLogger


class FeedbackCollector:
    """Collects user feedback on AI responses"""
    
    def __init__(self, logger: ConversationLogger):
        self.logger = logger
    
    def submit_feedback(
        self,
        example_id: str,
        score: int,
        comment: Optional[str] = None
    ) -> bool:
        """Submit user feedback (1-5 stars)"""
        if not 1 <= score <= 5:
            raise ValueError("Score must be between 1 and 5")
        
        self.logger.add_feedback(example_id, score)
        
        if comment:
            self._log_comment(example_id, comment)
        
        return True
    
    def _log_comment(self, example_id: str, comment: str):
        """Log feedback comment"""
        import json
        from pathlib import Path
        
        comments_file = Path(self.logger.log_dir) / "comments.jsonl"
        with open(comments_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "example_id": example_id,
                "comment": comment,
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")
