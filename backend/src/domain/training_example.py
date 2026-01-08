"""Training Example Domain Entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class TrainingExample:
    """Represents a training example for fine-tuning"""
    id: str
    user_message: str
    assistant_message: str
    context: Optional[str]
    feedback_score: Optional[int]  # 1-5 stars
    language: Optional[str]
    framework: Optional[str]
    complexity: int  # 0-10
    created_at: datetime
    metadata: Dict[str, Any]
    
    def to_jsonl(self) -> Dict[str, Any]:
        """Convert to JSONL format for fine-tuning"""
        messages = []
        if self.context:
            messages.append({"role": "system", "content": self.context})
        messages.append({"role": "user", "content": self.user_message})
        messages.append({"role": "assistant", "content": self.assistant_message})
        
        return {"messages": messages, "metadata": self.metadata}
    
    def is_high_quality(self) -> bool:
        """Check if example meets quality criteria"""
        return (
            self.feedback_score is None or self.feedback_score >= 4
        ) and len(self.assistant_message) >= 50
