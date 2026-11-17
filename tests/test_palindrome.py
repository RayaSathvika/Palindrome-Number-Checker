import pytest

from palindrome import is_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("racecar", True),
        ("Racecar", True),
        ("A man a plan a canal Panama", True),
        ("12321", True),
        ("121", True),
        ("hello", False),
        ("123", False),
        ("", False),
        ("   ", False),
        ("a", True),
    ],
)
def test_is_palindrome(value, expected):
    assert is_palindrome(value) is expected
