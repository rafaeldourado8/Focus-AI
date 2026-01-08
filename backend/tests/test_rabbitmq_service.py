"""
Unit tests for RabbitMQ service

Tests cover:
- Queue setup
- Message publishing
- Message consumption
- DLQ configuration
- Error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.infrastructure.queue.rabbitmq_service import RabbitMQService


class TestRabbitMQService:
    """Test RabbitMQ service functionality"""
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_connection_success(self, mock_connection):
        """Test successful RabbitMQ connection"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        service = RabbitMQService()
        
        assert service.connection is not None
        assert service.channel is not None
        mock_connection.assert_called_once()
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_queues_declared(self, mock_connection):
        """Test that all queues are declared"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        service = RabbitMQService()
        
        # Should declare 3 main queues + 3 DLQs = 6 total
        assert mock_channel.queue_declare.call_count == 6
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_publish_message(self, mock_connection):
        """Test message publishing"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        service = RabbitMQService()
        message = {"question": "test", "user_id": 1}
        
        result = service.publish(service.QUEUE_LLM_REQUESTS, message)
        
        assert result is True
        mock_channel.basic_publish.assert_called_once()
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_publish_failure(self, mock_connection):
        """Test publish failure handling"""
        mock_channel = Mock()
        mock_channel.basic_publish.side_effect = Exception("Connection lost")
        mock_connection.return_value.channel.return_value = mock_channel
        
        service = RabbitMQService()
        message = {"test": "data"}
        
        result = service.publish(service.QUEUE_LLM_REQUESTS, message)
        
        assert result is False
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_consume_setup(self, mock_connection):
        """Test consumer setup"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        service = RabbitMQService()
        callback = Mock()
        
        # Mock start_consuming to avoid blocking
        mock_channel.start_consuming.side_effect = KeyboardInterrupt
        
        try:
            service.consume(service.QUEUE_LLM_REQUESTS, callback)
        except KeyboardInterrupt:
            pass
        
        mock_channel.basic_qos.assert_called_once_with(prefetch_count=1)
        mock_channel.basic_consume.assert_called_once()
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_close_connection(self, mock_connection):
        """Test connection closing"""
        mock_conn = Mock()
        mock_conn.is_closed = False
        mock_connection.return_value = mock_conn
        
        service = RabbitMQService()
        service.close()
        
        mock_conn.close.assert_called_once()


class TestQueueNames:
    """Test queue name constants"""
    
    def test_queue_names_defined(self):
        """Test that queue names are properly defined"""
        assert RabbitMQService.QUEUE_LLM_REQUESTS == "llm.requests"
        assert RabbitMQService.QUEUE_LLM_RESPONSES == "llm.responses"
        assert RabbitMQService.QUEUE_TRAINING_DATA == "training.data"
    
    def test_dlq_suffix(self):
        """Test DLQ suffix"""
        assert RabbitMQService.DLQ_SUFFIX == ".dlq"


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_connection_failure(self, mock_connection):
        """Test connection failure raises exception"""
        mock_connection.side_effect = Exception("Connection refused")
        
        with pytest.raises(Exception):
            RabbitMQService()
    
    @patch('src.infrastructure.queue.rabbitmq_service.pika.BlockingConnection')
    def test_close_already_closed(self, mock_connection):
        """Test closing already closed connection"""
        mock_conn = Mock()
        mock_conn.is_closed = True
        mock_connection.return_value = mock_conn
        
        service = RabbitMQService()
        service.close()
        
        # Should not call close if already closed
        mock_conn.close.assert_not_called()
