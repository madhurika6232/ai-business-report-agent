import re


SENSITIVE_ERROR_PATTERNS = [
    # Windows paths
    r"[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]*",

    # Unix-style paths
    r"(?:/[^/\s]+){2,}",

    # Traceback markers
    r"Traceback \(most recent call last\):",

    # API keys / secrets
    r"(?i)(?:api[_-]?key|token|secret|password)"
    r"\s*[:=]\s*[^\s,;]+",
]


def sanitize_error(
    error: Exception | str,
) -> str:
    """Convert an internal error into a safe user-facing message."""

    message = str(error)

    sensitive = any(
        re.search(
            pattern,
            message,
        )
        for pattern in SENSITIVE_ERROR_PATTERNS
    )

    if sensitive:
        return (
            "The requested analysis could not be completed "
            "because of an internal processing error."
        )

    # Even non-sensitive errors should not expose arbitrary
    # implementation details to the end user.
    return (
        "The requested analysis could not be completed. "
        "Please try again or adjust the request."
    )


def build_safe_error_response(
    errors: list[Exception | str],
) -> str:
    """Create one safe response from one or more internal errors."""

    if not errors:
        return (
            "The requested analysis could not be completed."
        )

    return sanitize_error(
        errors[0]
    )