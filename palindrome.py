"""Palindrome checks for strings and numbers."""


def normalize(value: str) -> str:
    """Keep letters and digits, and compare them case-insensitively."""
    return "".join(ch.lower() for ch in value if ch.isalnum())


def is_palindrome(value: str) -> bool:
    """Return True when the meaningful characters read the same forwards and backwards."""
    normalized = normalize(value)
    return bool(normalized) and normalized == normalized[::-1]
