"""Tests for Training Data Collection"""
import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

from src.domain.training_example import TrainingExample
from src.infrastructure.training.conversation_logger import ConversationLogger
from src.infrastructure.training.data_curator import DataCurator
from src.infrastructure.training.feedback_collector import FeedbackCollector


class TestTrainingExample:
    def test_to_jsonl_with_context(self):
        example = TrainingExample(
            id="test123",
            user_message="How to use FastAPI?",
            assistant_message="FastAPI is a modern web framework...",
            context="You are a Python expert",
            feedback_score=5,
            language="python",
            framework="fastapi",
            complexity=3,
            created_at=datetime.utcnow(),
            metadata={"session": "abc"}
        )
        
        result = example.to_jsonl()
        assert len(result["messages"]) == 3
        assert result["messages"][0]["role"] == "system"
        assert result["messages"][1]["role"] == "user"
        assert result["messages"][2]["role"] == "assistant"
    
    def test_to_jsonl_without_context(self):
        example = TrainingExample(
            id="test123",
            user_message="Test",
            assistant_message="Response",
            context=None,
            feedback_score=None,
            language=None,
            framework=None,
            complexity=5,
            created_at=datetime.utcnow(),
            metadata={}
        )
        
        result = example.to_jsonl()
        assert len(result["messages"]) == 2
    
    def test_is_high_quality_with_good_feedback(self):
        example = TrainingExample(
            id="test123",
            user_message="Test",
            assistant_message="A" * 100,
            context=None,
            feedback_score=4,
            language=None,
            framework=None,
            complexity=5,
            created_at=datetime.utcnow(),
            metadata={}
        )
        
        assert example.is_high_quality()
    
    def test_is_high_quality_with_bad_feedback(self):
        example = TrainingExample(
            id="test123",
            user_message="Test",
            assistant_message="A" * 100,
            context=None,
            feedback_score=2,
            language=None,
            framework=None,
            complexity=5,
            created_at=datetime.utcnow(),
            metadata={}
        )
        
        assert not example.is_high_quality()
    
    def test_is_high_quality_short_response(self):
        example = TrainingExample(
            id="test123",
            user_message="Test",
            assistant_message="Short",
            context=None,
            feedback_score=5,
            language=None,
            framework=None,
            complexity=5,
            created_at=datetime.utcnow(),
            metadata={}
        )
        
        assert not example.is_high_quality()


class TestConversationLogger:
    @pytest.fixture
    def temp_log_dir(self, tmp_path):
        return str(tmp_path / "logs")
    
    @pytest.fixture
    def logger(self, temp_log_dir):
        return ConversationLogger(log_dir=temp_log_dir)
    
    def test_log_conversation(self, logger):
        example_id = logger.log_conversation(
            user_id="user123",
            session_id="session456",
            user_message="How to use Docker?",
            assistant_message="Docker is a containerization platform...",
            language="docker",
            complexity=4
        )
        
        assert example_id is not None
        assert len(example_id) == 16
    
    def test_log_creates_file(self, logger, temp_log_dir):
        logger.log_conversation(
            user_id="user123",
            session_id="session456",
            user_message="Test",
            assistant_message="Response"
        )
        
        log_dir = Path(temp_log_dir)
        files = list(log_dir.glob("conversations_*.jsonl"))
        assert len(files) == 1
    
    def test_add_feedback(self, logger, temp_log_dir):
        logger.add_feedback("example123", 5)
        
        feedback_file = Path(temp_log_dir) / "feedback.jsonl"
        assert feedback_file.exists()
        
        with open(feedback_file, "r") as f:
            data = json.loads(f.readline())
            assert data["example_id"] == "example123"
            assert data["score"] == 5
    
    def test_anonymize_user_id(self, logger):
        user_id = "user@example.com"
        anonymized = logger._anonymize(user_id)
        
        assert anonymized != user_id
        assert len(anonymized) == 16
        assert logger._anonymize(user_id) == anonymized  # Consistent


class TestDataCurator:
    @pytest.fixture
    def temp_dirs(self, tmp_path):
        log_dir = tmp_path / "logs"
        output_dir = tmp_path / "curated"
        log_dir.mkdir()
        return str(log_dir), str(output_dir)
    
    @pytest.fixture
    def curator(self, temp_dirs):
        log_dir, output_dir = temp_dirs
        return DataCurator(log_dir=log_dir, output_dir=output_dir)
    
    def test_load_examples(self, curator, temp_dirs):
        log_dir, _ = temp_dirs
        log_file = Path(log_dir) / "conversations_2024-01-15.jsonl"
        
        with open(log_file, "w") as f:
            f.write(json.dumps({
                "id": "test123",
                "user_message": "Test",
                "assistant_message": "Response",
                "context": None,
                "language": "python",
                "framework": None,
                "complexity": 5,
                "created_at": datetime.utcnow().isoformat(),
                "metadata": {}
            }) + "\n")
        
        examples = curator.load_examples()
        assert len(examples) == 1
        assert examples[0].id == "test123"
    
    def test_filter_high_quality(self, curator):
        examples = [
            TrainingExample(
                id="good",
                user_message="Test",
                assistant_message="A" * 100,
                context=None,
                feedback_score=5,
                language=None,
                framework=None,
                complexity=5,
                created_at=datetime.utcnow(),
                metadata={}
            ),
            TrainingExample(
                id="bad",
                user_message="Test",
                assistant_message="Short",
                context=None,
                feedback_score=2,
                language=None,
                framework=None,
                complexity=5,
                created_at=datetime.utcnow(),
                metadata={}
            )
        ]
        
        filtered = curator.filter_high_quality(examples)
        assert len(filtered) == 1
        assert filtered[0].id == "good"
    
    def test_export_for_training(self, curator):
        examples = [
            TrainingExample(
                id="test123",
                user_message="Test",
                assistant_message="Response",
                context=None,
                feedback_score=5,
                language="python",
                framework=None,
                complexity=5,
                created_at=datetime.utcnow(),
                metadata={}
            )
        ]
        
        output_file = curator.export_for_training(examples)
        assert Path(output_file).exists()
        
        with open(output_file, "r") as f:
            data = json.loads(f.readline())
            assert "messages" in data
    
    def test_get_statistics(self, curator):
        examples = [
            TrainingExample(
                id="1",
                user_message="Test",
                assistant_message="A" * 100,
                context=None,
                feedback_score=5,
                language="python",
                framework="fastapi",
                complexity=3,
                created_at=datetime.utcnow(),
                metadata={}
            ),
            TrainingExample(
                id="2",
                user_message="Test",
                assistant_message="A" * 100,
                context=None,
                feedback_score=4,
                language="python",
                framework="django",
                complexity=7,
                created_at=datetime.utcnow(),
                metadata={}
            )
        ]
        
        stats = curator.get_statistics(examples)
        assert stats["total_examples"] == 2
        assert stats["high_quality_examples"] == 2
        assert stats["languages"]["python"] == 2
        assert stats["avg_complexity"] == 5.0


class TestFeedbackCollector:
    @pytest.fixture
    def logger(self):
        return Mock(spec=ConversationLogger)
    
    @pytest.fixture
    def collector(self, logger):
        return FeedbackCollector(logger)
    
    def test_submit_feedback_valid(self, collector, logger):
        result = collector.submit_feedback("example123", 5)
        
        assert result is True
        logger.add_feedback.assert_called_once_with("example123", 5)
    
    def test_submit_feedback_invalid_score(self, collector):
        with pytest.raises(ValueError):
            collector.submit_feedback("example123", 6)
        
        with pytest.raises(ValueError):
            collector.submit_feedback("example123", 0)
    
    def test_submit_feedback_with_comment(self, collector, logger, tmp_path):
        logger.log_dir = tmp_path
        
        collector.submit_feedback("example123", 4, "Great response!")
        
        comments_file = tmp_path / "comments.jsonl"
        assert comments_file.exists()
