"""
Content filtering utilities for child safety.
"""
import re

# List of unsafe keywords for children
UNSAFE_KEYWORDS = {
    "violence": ["kill", "hate", "hurt", "attack", "weapon"],
    "adult": ["alcohol", "drug", "inappropriate"],
    "scary": ["ghost", "monster", "scary"]  # Can be customized
}

def is_safe_for_children(text: str) -> bool:
    """
    Check if text is safe for children.
    
    Args:
        text: Text to check
    
    Returns:
        bool: True if safe, False if contains unsafe content
    """
    text_lower = text.lower()
    
    for category, keywords in UNSAFE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', text_lower):
                return False
    
    return True

def sanitize_ai_response(response: str) -> str:
    """
    Clean AI response to ensure it's child-safe.
    
    Args:
        response: Raw AI response
    
    Returns:
        str: Sanitized response
    """
    # Remove any potentially unsafe content
    if not is_safe_for_children(response):
        return "Great reading! Keep practicing!"
    
    return response

def filter_reading_passage(passage_text: str) -> bool:
    """
    Check if a reading passage is age-appropriate.
    
    Args:
        passage_text: The passage content
    
    Returns:
        bool: True if appropriate, False otherwise
    """
    return is_safe_for_children(passage_text)
