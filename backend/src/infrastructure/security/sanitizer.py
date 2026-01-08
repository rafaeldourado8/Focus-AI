"""
Input Sanitization

Prevents XSS, SQL Injection, and other attacks
"""

import re
import html
from typing import Any


class InputSanitizer:
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 10000) -> str:
        """Sanitize user input string"""
        if not isinstance(text, str):
            return ""
        
        # Truncate
        text = text[:max_length]
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML to prevent XSS"""
        return html.escape(text)
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """Basic SQL injection prevention"""
        dangerous_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
            r"(--|;|\/\*|\*\/)",
            r"(\bOR\b.*=.*)",
            r"(\bAND\b.*=.*)"
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                raise ValueError("Potentially malicious input detected")
        
        return text
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove path traversal
        filename = filename.replace('../', '').replace('..\\', '')
        
        # Allow only safe characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        
        # Limit length
        return filename[:255]
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def sanitize_dict(data: dict) -> dict:
        """Recursively sanitize dictionary"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputSanitizer.sanitize_string(v) if isinstance(v, str) else v
                    for v in value
                ]
            else:
                sanitized[key] = value
        return sanitized
