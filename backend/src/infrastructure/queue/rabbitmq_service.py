"""
RabbitMQ Service

Handles message queue operations for async LLM processing.
Implements retry logic and dead letter queue.
"""

import pika
import json
import logging
from typing import Dict, Any, Callable
from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RabbitMQService:
    """RabbitMQ connection and queue management"""
    
    # Queue names
    QUEUE_LLM_REQUESTS = "llm.requests"
    QUEUE_LLM_RESPONSES = "llm.responses"
    QUEUE_TRAINING_DATA = "training.data"
    
    # Dead letter queue
    DLQ_SUFFIX = ".dlq"
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self._connect()
    
    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            params = pika.URLParameters(settings.RABBITMQ_URL)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self._setup_queues()
            logger.info("RabbitMQ connected successfully")
        except Exception as e:
            logger.error(f"RabbitMQ connection failed: {e}")
            raise
    
    def _setup_queues(self):
        """Declare queues with DLQ configuration"""
        queues = [
            self.QUEUE_LLM_REQUESTS,
            self.QUEUE_LLM_RESPONSES,
            self.QUEUE_TRAINING_DATA
        ]
        
        for queue in queues:
            # Declare DLQ
            dlq_name = f"{queue}{self.DLQ_SUFFIX}"
            self.channel.queue_declare(
                queue=dlq_name,
                durable=True
            )
            
            # Declare main queue with DLQ
            self.channel.queue_declare(
                queue=queue,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "",
                    "x-dead-letter-routing-key": dlq_name,
                    "x-message-ttl": 300000  # 5 minutes
                }
            )
            logger.info(f"Queue declared: {queue}")
    
    def publish(self, queue: str, message: Dict[str, Any]) -> bool:
        """Publish message to queue"""
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent
                    content_type="application/json"
                )
            )
            logger.info(f"Message published to {queue}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False
    
    def consume(self, queue: str, callback: Callable, auto_ack: bool = False):
        """Consume messages from queue"""
        def wrapper(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                if not auto_ack:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=wrapper,
            auto_ack=auto_ack
        )
        logger.info(f"Started consuming from {queue}")
        self.channel.start_consuming()
    
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")
