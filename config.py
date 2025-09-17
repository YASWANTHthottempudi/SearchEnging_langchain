"""
Configuration file for Yaswanth's AI Search Engine
Contains all customizable settings and constants
"""

import os
from typing import Dict, List

# Application Settings
APP_CONFIG = {
    "name": "Yaswanth's AI Search Engine",
    "version": "1.0.0",
    "author": "Yaswanth Thottempudi",
    "description": "Advanced Multi-Source AI Search Platform",
    "github_url": "https://github.com/yaswanththottempudi/ai-search-engine"
}

# Search Engine Settings
SEARCH_CONFIG = {
    "default_sources": ["Wikipedia", "ArXiv", "Web Search"],
    "max_results_per_source": 2,
    "default_response_length": "Medium",
    "search_timeout": 30,
    "supported_models": [
        "Gemma2-9b-it",
        "Llama-3.1-70b-versatile",
        "Mixtral-8x7b-32768"
    ]
}

# UI/UX Settings
UI_CONFIG = {
    "theme": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "success_color": "#28a745",
        "warning_color": "#ffc107",
        "error_color": "#dc3545"
    },
    "layout": {
        "page_title": "🔍 Yaswanth's AI Search Engine",
        "page_icon": "🔍",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
}

# API Configuration
API_CONFIG = {
    "groq_base_url": "https://api.groq.com/openai/v1",
    "default_model": "Gemma2-9b-it",
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 30
}

# Search Sources Configuration
SEARCH_SOURCES = {
    "Wikipedia": {
        "enabled": True,
        "max_results": 2,
        "content_length": 500,
        "description": "Comprehensive encyclopedia articles"
    },
    "ArXiv": {
        "enabled": True,
        "max_results": 2,
        "content_length": 500,
        "description": "Latest research papers and academic content"
    },
    "Web Search": {
        "enabled": True,
        "max_results": 3,
        "content_length": 300,
        "description": "Real-time web search results"
    }
}

# Feature Flags
FEATURES = {
    "search_history": True,
    "export_functionality": True,
    "advanced_settings": True,
    "statistics_tracking": True,
    "custom_styling": True,
    "multi_source_search": True
}

# Error Messages
ERROR_MESSAGES = {
    "no_api_key": "⚠️ Please enter your Groq API key in the sidebar to start searching!",
    "no_sources": "⚠️ Please select at least one search source!",
    "search_failed": "❌ Search failed. Please try again or check your API key.",
    "invalid_input": "❌ Invalid input. Please provide a valid search query.",
    "timeout_error": "⏰ Search timed out. Please try a simpler query."
}

# Success Messages
SUCCESS_MESSAGES = {
    "search_complete": "✅ Search completed successfully!",
    "history_exported": "📥 Search history exported successfully!",
    "settings_saved": "💾 Settings saved successfully!"
}

# Default Prompts
DEFAULT_PROMPTS = {
    "welcome": "👋 Welcome to my AI Search Engine! I can help you search across Wikipedia, ArXiv research papers, and the web. What would you like to explore today?",
    "placeholder": "Ask me anything! Try: 'What is quantum computing?' or 'Latest AI research papers'",
    "help": "💡 Try asking about:\n• Scientific concepts\n• Recent research papers\n• Current events\n• Technical topics\n• Historical information"
}

def get_config(section: str) -> Dict:
    """Get configuration for a specific section"""
    configs = {
        "app": APP_CONFIG,
        "search": SEARCH_CONFIG,
        "ui": UI_CONFIG,
        "api": API_CONFIG,
        "sources": SEARCH_SOURCES,
        "features": FEATURES,
        "errors": ERROR_MESSAGES,
        "success": SUCCESS_MESSAGES,
        "prompts": DEFAULT_PROMPTS
    }
    return configs.get(section, {})

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURES.get(feature, False)

def get_search_source_config(source: str) -> Dict:
    """Get configuration for a specific search source"""
    return SEARCH_SOURCES.get(source, {})
