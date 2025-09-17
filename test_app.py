"""
Test suite for Yaswanth's AI Search Engine
Tests core functionality and utilities
"""

import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    validate_api_key,
    format_search_query,
    extract_keywords,
    calculate_search_score,
    truncate_text,
    validate_search_sources
)

class TestUtils:
    """Test utility functions"""
    
    def test_validate_api_key(self):
        """Test API key validation"""
        # Valid API key
        assert validate_api_key("gsk_1234567890abcdef1234567890abcdef") == True
        
        # Invalid API keys
        assert validate_api_key("") == False
        assert validate_api_key("invalid_key") == False
        assert validate_api_key("gsk_short") == False
        assert validate_api_key(None) == False
    
    def test_format_search_query(self):
        """Test search query formatting"""
        # Normal query
        assert format_search_query("  hello   world  ") == "hello world"
        
        # Query with special characters
        assert format_search_query("hello@#$%world") == "helloworld"
        
        # Empty query
        assert format_search_query("") == ""
        assert format_search_query(None) == ""
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        query = "What is machine learning and how does it work?"
        keywords = extract_keywords(query)
        
        # Should extract meaningful keywords
        assert "machine" in keywords
        assert "learning" in keywords
        assert "work" in keywords
        
        # Should not include stop words
        assert "what" not in keywords
        assert "is" not in keywords
        assert "and" not in keywords
        assert "how" not in keywords
        assert "does" not in keywords
        assert "it" not in keywords
    
    def test_calculate_search_score(self):
        """Test search score calculation"""
        query = "machine learning"
        result = "Machine learning is a subset of artificial intelligence"
        
        score = calculate_search_score(query, result)
        assert 0 <= score <= 1
        assert score > 0  # Should have some relevance
        
        # Test with no keywords
        score_empty = calculate_search_score("", result)
        assert score_empty == 0.0
    
    def test_truncate_text(self):
        """Test text truncation"""
        long_text = "This is a very long text that should be truncated"
        
        # Test truncation
        truncated = truncate_text(long_text, 20)
        assert len(truncated) <= 20
        assert truncated.endswith("...")
        
        # Test no truncation needed
        short_text = "Short text"
        assert truncate_text(short_text, 20) == short_text
    
    def test_validate_search_sources(self):
        """Test search source validation"""
        sources = ["Wikipedia", "ArXiv", "InvalidSource", "Web Search"]
        valid_sources = validate_search_sources(sources)
        
        assert "Wikipedia" in valid_sources
        assert "ArXiv" in valid_sources
        assert "Web Search" in valid_sources
        assert "InvalidSource" not in valid_sources

class TestConfig:
    """Test configuration functions"""
    
    def test_config_import(self):
        """Test that config can be imported"""
        try:
            from config import get_config, is_feature_enabled, get_search_source_config
            assert callable(get_config)
            assert callable(is_feature_enabled)
            assert callable(get_search_source_config)
        except ImportError:
            pytest.fail("Config module could not be imported")

def test_app_imports():
    """Test that main app can be imported without errors"""
    try:
        # This will test if all imports work correctly
        import app
        assert hasattr(app, 'st')
        assert hasattr(app, 'ChatGroq')
    except ImportError as e:
        pytest.fail(f"App module could not be imported: {e}")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
