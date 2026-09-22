import pytest

from src.guardrails.input_validation import (
    MAX_QUERY_LENGTH,
    normalize_user_query,
)


def test_normal_query():
    result = normalize_user_query(
        "Which sellers have the worst delivery performance?"
    )

    assert result == (
        "Which sellers have the worst delivery performance?"
    )


def test_whitespace_normalization():
    result = normalize_user_query(
        " Revenue\n\nby\tstate "
    )

    assert result == "Revenue by state"


def test_empty_query_rejected():
    with pytest.raises(
        ValueError,
        match="user_query cannot be empty",
    ):
        normalize_user_query("")


def test_whitespace_query_rejected():
    with pytest.raises(
        ValueError,
        match="user_query cannot be empty",
    ):
        normalize_user_query("   ")


def test_non_string_rejected():
    with pytest.raises(
        TypeError,
        match="user_query must be a string",
    ):
        normalize_user_query(123)


def test_long_query_rejected():
    query = "a" * (
        MAX_QUERY_LENGTH + 1
    )

    with pytest.raises(
        ValueError,
        match="exceeds maximum length",
    ):
        normalize_user_query(query)


def test_control_character_rejected():
    with pytest.raises(
        ValueError,
        match="control characters",
    ):
        normalize_user_query(
            "test\x00query"
        )