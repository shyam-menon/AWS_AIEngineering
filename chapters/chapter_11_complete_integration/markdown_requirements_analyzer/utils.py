#!/usr/bin/env python3
"""
Utility Functions

This module provides common utility functions for validation, error handling,
logging, and other shared functionality across the markdown requirements analyzer.
"""

import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def print_error(message: str):
    """Print error message with consistent formatting."""
    try:
        print(f"❌ ERROR: {message}", file=sys.stderr)
    except UnicodeEncodeError:
        print(f"ERROR: {message}", file=sys.stderr)


def print_warning(message: str):
    """Print warning message with consistent formatting."""
    try:
        print(f"⚠️  WARNING: {message}")
    except UnicodeEncodeError:
        print(f"WARNING: {message}")


def print_info(message: str):
    """Print info message with consistent formatting."""
    try:
        print(f"ℹ️  INFO: {message}")
    except UnicodeEncodeError:
        print(f"INFO: {message}")


def print_success(message: str):
    """Print success message with consistent formatting."""
    try:
        print(f"✅ SUCCESS: {message}")
    except UnicodeEncodeError:
        print(f"SUCCESS: {message}")


def validate_file_path(file_path: Union[str, Path], extensions: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Validate that a file path exists and has the correct extension.
    
    Args:
        file_path: Path to validate
        extensions: List of allowed extensions (e.g., ['.md', '.markdown'])
        
    Returns:
        Validation result dictionary
    """
    file_path = Path(file_path)
    
    result = {
        'valid': True,
        'issues': [],
        'path': file_path,
        'exists': False,
        'is_file': False,
        'extension': None
    }
    
    # Check if path exists
    if not file_path.exists():
        result['valid'] = False
        result['issues'].append(f"File does not exist: {file_path}")
        return result
    
    result['exists'] = True
    
    # Check if it's a file
    if not file_path.is_file():
        result['valid'] = False
        result['issues'].append(f"Path is not a file: {file_path}")
        return result
    
    result['is_file'] = True
    result['extension'] = file_path.suffix.lower()
    
    # Check extension if specified
    if extensions:
        extensions = [ext.lower() for ext in extensions]
        if result['extension'] not in extensions:
            result['valid'] = False
            result['issues'].append(f"Invalid file extension. Expected {extensions}, got {result['extension']}")
    
    return result


def validate_directory_path(directory_path: Union[str, Path], create_if_missing: bool = False) -> Dict[str, Any]:
    """
    Validate that a directory path exists or can be created.
    
    Args:
        directory_path: Path to validate
        create_if_missing: Whether to create the directory if it doesn't exist
        
    Returns:
        Validation result dictionary
    """
    directory_path = Path(directory_path)
    
    result = {
        'valid': True,
        'issues': [],
        'path': directory_path,
        'exists': False,
        'is_directory': False,
        'created': False
    }
    
    # Check if path exists
    if not directory_path.exists():
        if create_if_missing:
            try:
                directory_path.mkdir(parents=True, exist_ok=True)
                result['created'] = True
                result['exists'] = True
                result['is_directory'] = True
            except Exception as e:
                result['valid'] = False
                result['issues'].append(f"Could not create directory: {str(e)}")
                return result
        else:
            result['valid'] = False
            result['issues'].append(f"Directory does not exist: {directory_path}")
            return result
    else:
        result['exists'] = True
    
    # Check if it's a directory
    if not directory_path.is_dir():
        result['valid'] = False
        result['issues'].append(f"Path is not a directory: {directory_path}")
        return result
    
    result['is_directory'] = True
    return result


def safe_json_parse(json_str: str) -> Optional[Dict]:
    """
    Safely parse JSON string with error handling.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    try:
        # Clean the JSON string
        cleaned = json_str.strip()
        
        # Remove markdown code blocks if present
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        # Find JSON content between braces
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_content = cleaned[start_idx:end_idx + 1]
            return json.loads(json_content)
        else:
            return json.loads(cleaned)
            
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parsing failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {str(e)}")
        return None


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename to be safe for filesystem use.
    
    Args:
        filename: Original filename
        max_length: Maximum length for the filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    # Trim whitespace and dots from ends
    sanitized = sanitized.strip(' .')
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = 'unnamed_file'
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def generate_timestamp_filename(base_name: str, extension: str = '', timestamp_format: str = '%Y%m%d_%H%M%S') -> str:
    """
    Generate a filename with timestamp.
    
    Args:
        base_name: Base name for the file
        extension: File extension (with or without dot)
        timestamp_format: Format for timestamp
        
    Returns:
        Filename with timestamp
    """
    timestamp = datetime.now().strftime(timestamp_format)
    
    if extension and not extension.startswith('.'):
        extension = f'.{extension}'
    
    return f"{base_name}_{timestamp}{extension}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def deep_merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        base: Base dictionary
        override: Dictionary with override values
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_json_structure(data: Any, required_fields: List[str] = None) -> Dict[str, Any]:
    """
    Validate JSON data structure.
    
    Args:
        data: Data to validate
        required_fields: List of required field names
        
    Returns:
        Validation result
    """
    result = {
        'valid': True,
        'issues': [],
        'type': type(data).__name__,
        'fields_present': [],
        'fields_missing': []
    }
    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        result['valid'] = False
        result['issues'].append(f"Expected dictionary, got {type(data).__name__}")
        return result
    
    # Check for required fields
    if required_fields:
        result['fields_present'] = [field for field in required_fields if field in data]
        result['fields_missing'] = [field for field in required_fields if field not in data]
        
        if result['fields_missing']:
            result['valid'] = False
            result['issues'].append(f"Missing required fields: {result['fields_missing']}")
    
    return result


def setup_logging(level: str = 'INFO', 
                 log_file: Optional[Union[str, Path]] = None,
                 format_string: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        level: Logging level
        log_file: Optional log file path
        format_string: Optional format string
        
    Returns:
        Configured logger
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[]
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(format_string))
    logging.getLogger().addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_string))
        logging.getLogger().addHandler(file_handler)
    
    return logging.getLogger(__name__)


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a simple text progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        width: Width of progress bar
        
    Returns:
        Progress bar string
    """
    if total == 0:
        return f"[{'#' * width}] 100%"
    
    percentage = min(100, int((current / total) * 100))
    filled = int((current / total) * width)
    bar = '#' * filled + '-' * (width - filled)
    
    return f"[{bar}] {percentage}%"


def retry_operation(operation, max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Retry an operation with exponential backoff.
    
    Args:
        operation: Function to retry
        max_retries: Maximum number of retries
        delay: Initial delay between retries
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Result of successful operation
        
    Raises:
        Last exception if all retries fail
    """
    import time
    
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except exceptions as e:
            if attempt == max_retries:
                raise e
            
            wait_time = delay * (2 ** attempt)
            logger.warning(f"Operation failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
            logger.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate basic text similarity using simple metrics.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    # Simple word-based similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 and not words2:
        return 1.0
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def extract_keywords(text: str, min_length: int = 3, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple frequency analysis.
    
    Args:
        text: Text to analyze
        min_length: Minimum word length
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords
    """
    import re
    from collections import Counter
    
    # Common stop words to filter out
    stop_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
        'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
        'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
        'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
        'one', 'all', 'would', 'there', 'their', 'what', 'so',
        'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me'
    }
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter words
    filtered_words = [
        word for word in words 
        if len(word) >= min_length and word not in stop_words
    ]
    
    # Count frequencies
    word_counts = Counter(filtered_words)
    
    # Return top keywords
    return [word for word, count in word_counts.most_common(max_keywords)]


if __name__ == "__main__":
    # Test utility functions
    print("🧪 Testing Utility Functions")
    print("=" * 40)
    
    # Test file validation
    test_file = Path(__file__)
    validation = validate_file_path(test_file, ['.py'])
    print(f"File validation: {validation['valid']}")
    
    # Test JSON parsing
    test_json = '{"test": "value", "number": 42}'
    parsed = safe_json_parse(test_json)
    print(f"JSON parsing: {parsed}")
    
    # Test filename sanitization
    unsafe_name = 'test<>file:|*.txt'
    safe_name = sanitize_filename(unsafe_name)
    print(f"Filename sanitization: '{unsafe_name}' -> '{safe_name}'")
    
    # Test timestamp filename
    timestamp_name = generate_timestamp_filename('report', 'json')
    print(f"Timestamp filename: {timestamp_name}")
    
    # Test file size formatting
    size = format_file_size(1536)
    print(f"File size formatting: 1536 bytes -> {size}")
    
    # Test text truncation
    long_text = "This is a very long text that should be truncated"
    short_text = truncate_text(long_text, 20)
    print(f"Text truncation: '{short_text}'")
    
    # Test progress bar
    progress = create_progress_bar(7, 10)
    print(f"Progress bar: {progress}")
    
    print("\n✅ All utility function tests completed!")