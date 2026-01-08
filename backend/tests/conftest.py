import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/"
os.environ["JWT_SECRET"] = "test-secret-key"
os.environ["GEMINI_API_KEY"] = "test-api-key"
os.environ["OPENAI_API_KEY"] = "test-api-key"

@pytest.fixture(autouse=True)
def reset_env():
    yield