import re


MAX_QUERY_LENGTH = 2000


def normalize_user_query(
    user_query: str,
) -> str:
    """Normalize and validate a user query."""

    if not isinstance(
        user_query,
        str,
    ):
        raise TypeError(
            "user_query must be a string."
        )

    # Normalize whitespace.
    normalized = re.sub(
        r"\s+",
        " ",
        user_query,
    ).strip()

    if not normalized:
        raise ValueError(
            "user_query cannot be empty."
        )

    if len(normalized) > MAX_QUERY_LENGTH:
        raise ValueError(
            f"user_query exceeds maximum length "
            f"of {MAX_QUERY_LENGTH} characters."
        )

    # Reject unsafe ASCII control characters.
    control_characters = [
        character
        for character in normalized
        if ord(character) < 32
        and character not in {
            "\t",
            "\n",
            "\r",
        }
    ]

    if control_characters:
        raise ValueError(
            "user_query contains unsupported "
            "control characters."
        )

    return normalized