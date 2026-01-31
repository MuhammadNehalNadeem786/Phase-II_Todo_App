import re
from typing import Any, Union
from html import escape


def sanitize_input(input_value: Any) -> Any:
    """
    Sanitize input values to prevent XSS and other injection attacks.

    Args:
        input_value: The input value to sanitize

    Returns:
        Sanitized input value
    """
    if isinstance(input_value, str):
        # Escape HTML characters
        sanitized = escape(input_value)

        # Remove potentially dangerous patterns
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

        return sanitized
    elif isinstance(input_value, dict):
        # Recursively sanitize dictionary values
        return {key: sanitize_input(value) for key, value in input_value.items()}
    elif isinstance(input_value, list):
        # Recursively sanitize list items
        return [sanitize_input(item) for item in input_value]
    else:
        # Return primitive values as-is
        return input_value


def validate_title(title: str) -> bool:
    """
    Validate task title.

    Args:
        title: The title to validate

    Returns:
        True if valid, False otherwise
    """
    if not title or not isinstance(title, str):
        return False

    if len(title) < 1 or len(title) > 255:
        return False

    # Check for potentially dangerous content
    if '<script' in title.lower() or 'javascript:' in title.lower():
        return False

    return True


def validate_description(description: Union[str, None]) -> bool:
    """
    Validate task description.

    Args:
        description: The description to validate

    Returns:
        True if valid, False otherwise
    """
    if description is None:
        return True

    if not isinstance(description, str):
        return False

    if len(description) > 1000:
        return False

    # Check for potentially dangerous content
    if '<script' in description.lower() or 'javascript:' in description.lower():
        return False

    return True


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID.

    Args:
        user_id: The user ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id or not isinstance(user_id, str):
        return False

    if len(user_id) < 1 or len(user_id) > 255:
        return False

    # Check for potentially dangerous content
    if '<script' in user_id.lower() or 'javascript:' in user_id.lower():
        return False

    return True