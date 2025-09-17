"""
Utility functions for Yaswanth's AI Search Engine
Contains helper functions for data processing, validation, and formatting
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st

def validate_api_key(api_key: str) -> bool:
    """
    Validate Groq API key format
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation - Groq API keys typically start with 'gsk_'
    return api_key.startswith('gsk_') and len(api_key) > 20

def format_search_query(query: str) -> str:
    """
    Clean and format search query
    
    Args:
        query (str): Raw search query
        
    Returns:
        str: Formatted search query
    """
    if not query:
        return ""
    
    # Remove extra whitespace
    query = re.sub(r'\s+', ' ', query.strip())
    
    # Remove special characters that might cause issues
    query = re.sub(r'[^\w\s\?\!\.\,\-]', '', query)
    
    return query

def extract_keywords(query: str) -> List[str]:
    """
    Extract keywords from search query
    
    Args:
        query (str): Search query
        
    Returns:
        List[str]: List of extracted keywords
    """
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'what', 'when', 'where', 'why', 'how', 'who'}
    
    # Extract words
    words = re.findall(r'\b\w+\b', query.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

def calculate_search_score(query: str, result: str) -> float:
    """
    Calculate relevance score for search results
    
    Args:
        query (str): Original search query
        result (str): Search result content
        
    Returns:
        float: Relevance score between 0 and 1
    """
    if not query or not result:
        return 0.0
    
    query_keywords = extract_keywords(query)
    result_lower = result.lower()
    
    if not query_keywords:
        return 0.0
    
    # Count keyword matches
    matches = sum(1 for keyword in query_keywords if keyword in result_lower)
    
    # Calculate score
    score = matches / len(query_keywords)
    
    return min(score, 1.0)

def format_timestamp(timestamp: str) -> str:
    """
    Format timestamp for display
    
    Args:
        timestamp (str): ISO timestamp
        
    Returns:
        str: Formatted timestamp
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp

def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to specified length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def create_search_summary(search_data: Dict) -> str:
    """
    Create a summary of search data
    
    Args:
        search_data (Dict): Search data dictionary
        
    Returns:
        str: Formatted summary
    """
    query = search_data.get('query', 'Unknown')
    timestamp = search_data.get('timestamp', 'Unknown')
    sources = search_data.get('sources', [])
    
    formatted_time = format_timestamp(timestamp)
    sources_str = ', '.join(sources) if sources else 'No sources'
    
    return f"**Query:** {query}\n**Time:** {formatted_time}\n**Sources:** {sources_str}"

def export_search_data(search_history: List[Dict], format_type: str = 'json') -> str:
    """
    Export search history in specified format
    
    Args:
        search_history (List[Dict]): List of search history items
        format_type (str): Export format ('json' or 'csv')
        
    Returns:
        str: Exported data as string
    """
    if format_type == 'json':
        return json.dumps(search_history, indent=2, default=str)
    elif format_type == 'csv':
        if not search_history:
            return ""
        
        # Create CSV header
        headers = ['timestamp', 'query', 'sources']
        csv_lines = [','.join(headers)]
        
        # Add data rows
        for item in search_history:
            row = [
                item.get('timestamp', ''),
                f'"{item.get("query", "")}"',
                f'"{",".join(item.get("sources", []))}"'
            ]
            csv_lines.append(','.join(row))
        
        return '\n'.join(csv_lines)
    
    return ""

def get_search_suggestions(query: str) -> List[str]:
    """
    Generate search suggestions based on query
    
    Args:
        query (str): Current search query
        
    Returns:
        List[str]: List of suggestions
    """
    suggestions = []
    
    # Common search patterns
    if 'what is' in query.lower():
        suggestions.extend([
            f"{query} definition",
            f"{query} explanation",
            f"{query} meaning"
        ])
    elif 'how to' in query.lower():
        suggestions.extend([
            f"{query} tutorial",
            f"{query} guide",
            f"{query} steps"
        ])
    elif 'latest' in query.lower() or 'recent' in query.lower():
        suggestions.extend([
            f"{query} 2024",
            f"{query} news",
            f"{query} updates"
        ])
    
    # Add generic suggestions
    suggestions.extend([
        f"{query} examples",
        f"{query} benefits",
        f"{query} applications"
    ])
    
    return suggestions[:5]  # Return top 5 suggestions

def validate_search_sources(sources: List[str]) -> List[str]:
    """
    Validate and filter search sources
    
    Args:
        sources (List[str]): List of source names
        
    Returns:
        List[str]: Validated source names
    """
    valid_sources = ['Wikipedia', 'ArXiv', 'Web Search']
    return [source for source in sources if source in valid_sources]

def create_progress_bar(current: int, total: int, label: str = "Progress") -> None:
    """
    Create a progress bar in Streamlit
    
    Args:
        current (int): Current progress
        total (int): Total items
        label (str): Progress bar label
    """
    if total > 0:
        progress = current / total
        st.progress(progress, text=f"{label}: {current}/{total}")

def log_search_activity(query: str, sources: List[str], success: bool = True) -> None:
    """
    Log search activity (placeholder for future logging implementation)
    
    Args:
        query (str): Search query
        sources (List[str]): Search sources used
        success (bool): Whether search was successful
    """
    # This could be extended to log to a file or database
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'query': query,
        'sources': sources,
        'success': success
    }
    
    # For now, just store in session state
    if 'search_logs' not in st.session_state:
        st.session_state.search_logs = []
    
    st.session_state.search_logs.append(log_entry)

def get_search_statistics() -> Dict[str, Any]:
    """
    Get search statistics from session state
    
    Returns:
        Dict[str, Any]: Search statistics
    """
    stats = {
        'total_searches': st.session_state.get('total_searches', 0),
        'successful_searches': 0,
        'failed_searches': 0,
        'most_used_sources': {},
        'average_query_length': 0
    }
    
    # Calculate statistics from search logs
    if 'search_logs' in st.session_state:
        logs = st.session_state.search_logs
        stats['successful_searches'] = sum(1 for log in logs if log.get('success', False))
        stats['failed_searches'] = len(logs) - stats['successful_searches']
        
        # Most used sources
        source_counts = {}
        query_lengths = []
        
        for log in logs:
            for source in log.get('sources', []):
                source_counts[source] = source_counts.get(source, 0) + 1
            query_lengths.append(len(log.get('query', '')))
        
        stats['most_used_sources'] = source_counts
        stats['average_query_length'] = sum(query_lengths) / len(query_lengths) if query_lengths else 0
    
    return stats
