"""
Tests for Input Sanitizer
"""

import pytest
from src.infrastructure.security.sanitizer import InputSanitizer


def test_sanitize_string_basic():
    """Test basic string sanitization"""
    result = InputSanitizer.sanitize_string("  Hello   World  ")
    assert result == "Hello World"


def test_sanitize_string_removes_null_bytes():
    """Test null byte removal"""
    result = InputSanitizer.sanitize_string("Hello\x00World")
    assert result == "HelloWorld"


def test_sanitize_string_truncates():
    """Test string truncation"""
    long_text = "a" * 20000
    result = InputSanitizer.sanitize_string(long_text, max_length=100)
    assert len(result) == 100


def test_sanitize_html():
    """Test HTML escaping"""
    result = InputSanitizer.sanitize_html("<script>alert('xss')</script>")
    assert "&lt;script&gt;" in result
    assert "<script>" not in result


def test_sanitize_sql_detects_injection():
    """Test SQL injection detection"""
    with pytest.raises(ValueError):
        InputSanitizer.sanitize_sql("SELECT * FROM users")
    
    with pytest.raises(ValueError):
        InputSanitizer.sanitize_sql("1' OR '1'='1")
    
    with pytest.raises(ValueError):
        InputSanitizer.sanitize_sql("DROP TABLE users")


def test_sanitize_sql_allows_safe_input():
    """Test that safe input passes"""
    result = InputSanitizer.sanitize_sql("Hello World")
    assert result == "Hello World"


def test_sanitize_filename():
    """Test filename sanitization"""
    result = InputSanitizer.sanitize_filename("../../etc/passwd")
    assert ".." not in result
    
    result = InputSanitizer.sanitize_filename("file<>name.txt")
    assert result == "file__name.txt"


def test_validate_email():
    """Test email validation"""
    assert InputSanitizer.validate_email("user@example.com") == True
    assert InputSanitizer.validate_email("invalid.email") == False
    assert InputSanitizer.validate_email("@example.com") == False
    assert InputSanitizer.validate_email("user@") == False


def test_sanitize_dict():
    """Test dictionary sanitization"""
    data = {
        "name": "  John  Doe  ",
        "email": "john@example.com",
        "nested": {
            "value": "  test  "
        },
        "list": ["  item1  ", "  item2  "]
    }
    
    result = InputSanitizer.sanitize_dict(data)
    
    assert result["name"] == "John Doe"
    assert result["nested"]["value"] == "test"
    assert result["list"][0] == "item1"


def test_sanitize_string_non_string_input():
    """Test handling of non-string input"""
    result = InputSanitizer.sanitize_string(123)
    assert result == ""
    
    result = InputSanitizer.sanitize_string(None)
    assert result == ""
