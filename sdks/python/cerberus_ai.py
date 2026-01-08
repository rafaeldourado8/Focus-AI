"""
Cerberus AI Python SDK

Official Python client for Cerberus AI API
"""

import requests
from typing import List, Dict, Optional, Any


class CerberusAI:
    """Cerberus AI API Client"""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "cerberus-pro",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        debug_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Create a chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (cerberus-lite, cerberus-pro, cerberus-debug)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            debug_mode: Enable debug mode for deep analysis
        
        Returns:
            Response dict with completion
        """
        response = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "debug_mode": debug_mode
            }
        )
        response.raise_for_status()
        return response.json()
    
    def analyze_code(
        self,
        code: str,
        language: str,
        checks: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze code for issues
        
        Args:
            code: Code to analyze
            language: Programming language
            checks: List of checks (security, performance, style)
        
        Returns:
            Analysis results
        """
        response = self.session.post(
            f"{self.base_url}/v1/code/analyze",
            json={
                "code": code,
                "language": language,
                "checks": checks or ["security", "performance", "style"]
            }
        )
        response.raise_for_status()
        return response.json()
    
    def debug_code(
        self,
        error: str,
        code: str,
        language: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Debug code with error
        
        Args:
            error: Error message
            code: Code that caused error
            language: Programming language
            context: Additional context
        
        Returns:
            Debug information with solutions
        """
        response = self.session.post(
            f"{self.base_url}/v1/code/debug",
            json={
                "error": error,
                "code": code,
                "language": language,
                "context": context
            }
        )
        response.raise_for_status()
        return response.json()
    
    def refactor_code(
        self,
        code: str,
        language: str,
        goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Refactor code
        
        Args:
            code: Code to refactor
            language: Programming language
            goals: Refactoring goals (readability, maintainability)
        
        Returns:
            Refactored code and explanation
        """
        response = self.session.post(
            f"{self.base_url}/v1/code/refactor",
            json={
                "code": code,
                "language": language,
                "goals": goals or ["readability", "maintainability"]
            }
        )
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> Dict[str, Any]:
        """List available models"""
        response = self.session.get(f"{self.base_url}/v1/models")
        response.raise_for_status()
        return response.json()
    
    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics"""
        response = self.session.get(f"{self.base_url}/v1/usage")
        response.raise_for_status()
        return response.json()
