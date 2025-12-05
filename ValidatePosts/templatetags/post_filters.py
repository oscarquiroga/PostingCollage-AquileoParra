"""
Custom Django template filters for cleaning HTML content.
"""
import re
from django import template

register = template.Library()


@register.filter
def clean_html(value):
    """
    Remove all HTML tags and clean formatting from text.
    Handles:
    - All HTML tags (<p>, <span>, <strong>, <em>, <u>, etc.)
    - Multiple spaces/newlines
    - Preserves line breaks as spaces
    
    Usage: {{ post.body|clean_html|truncatewords:20 }}
    """
    if not value:
        return ''
    
    # Remove all HTML tags
    clean = re.sub(r'<[^>]+>', '', str(value))
    
    # Replace multiple spaces with single space
    clean = re.sub(r'\s+', ' ', clean)
    
    # Strip leading/trailing whitespace
    clean = clean.strip()
    
    return clean
