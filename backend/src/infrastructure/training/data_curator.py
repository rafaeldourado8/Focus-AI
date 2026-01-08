"""Data Curator for Training Example Quality Control"""
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.domain.training_example import TrainingExample


class DataCurator:
    """Curates and filters training examples"""
    
    def __init__(self, log_dir: str = "data/training_logs", output_dir: str = "data/curated"):
        self.log_dir = Path(log_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_examples(self, date: Optional[str] = None) -> List[TrainingExample]:
        """Load examples from logs"""
        examples = []
        pattern = f"conversations_{date}.jsonl" if date else "conversations_*.jsonl"
        
        for log_file in self.log_dir.glob(pattern):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    examples.append(TrainingExample(
                        id=data["id"],
                        user_message=data["user_message"],
                        assistant_message=data["assistant_message"],
                        context=data.get("context"),
                        feedback_score=None,
                        language=data.get("language"),
                        framework=data.get("framework"),
                        complexity=data["complexity"],
                        created_at=datetime.fromisoformat(data["created_at"]),
                        metadata=data["metadata"]
                    ))
        
        return examples
    
    def apply_feedback(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Apply user feedback scores to examples"""
        feedback_file = self.log_dir / "feedback.jsonl"
        if not feedback_file.exists():
            return examples
        
        feedback_map = {}
        with open(feedback_file, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                feedback_map[data["example_id"]] = data["score"]
        
        for example in examples:
            if example.id in feedback_map:
                example.feedback_score = feedback_map[example.id]
        
        return examples
    
    def filter_high_quality(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Filter only high-quality examples"""
        return [ex for ex in examples if ex.is_high_quality()]
    
    def export_for_training(self, examples: List[TrainingExample], filename: str = "training_data.jsonl"):
        """Export curated examples in fine-tuning format"""
        output_file = self.output_dir / filename
        
        with open(output_file, "w", encoding="utf-8") as f:
            for example in examples:
                f.write(json.dumps(example.to_jsonl()) + "\n")
        
        return str(output_file)
    
    def get_statistics(self, examples: List[TrainingExample]) -> dict:
        """Get dataset statistics"""
        total = len(examples)
        high_quality = len([ex for ex in examples if ex.is_high_quality()])
        
        languages = {}
        frameworks = {}
        for ex in examples:
            if ex.language:
                languages[ex.language] = languages.get(ex.language, 0) + 1
            if ex.framework:
                frameworks[ex.framework] = frameworks.get(ex.framework, 0) + 1
        
        return {
            "total_examples": total,
            "high_quality_examples": high_quality,
            "quality_rate": high_quality / total if total > 0 else 0,
            "languages": languages,
            "frameworks": frameworks,
            "avg_complexity": sum(ex.complexity for ex in examples) / total if total > 0 else 0
        }
