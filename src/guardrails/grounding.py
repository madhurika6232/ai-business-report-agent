import re
from typing import Any


def extract_business_numbers(
    text: str,
) -> list[float]:
    """Extract business metrics while ignoring dates, IDs, and range labels."""

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string."
        )

    # Remove long hexadecimal / anonymized identifiers.
    text = re.sub(
        r"\b[a-fA-F0-9]{20,}\b",
        "",
        text,
    )

    # Remove dates such as 2018-03 and 2018-03-01.
    text = re.sub(
        r"\b\d{4}[--–]\d{2}(?:[--–]\d{2})?\b",
        "",
        text,
    )

    # Remove ranges such as 4-7 days and 8–14 days.
    text = re.sub(
        r"\b\d+\s*[--–]\s*\d+\s+days?\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove labels such as 15+ days.
    text = re.sub(
        r"\b\d+\+\s+days?\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove numbered-list markers.
    text = re.sub(
        r"(?m)^\s*\d+\.\s+",
        "",
        text,
    )

    matches = re.findall(
        r"(?<![\w])[-+]?\d[\d,]*(?:\.\d+)?(?![\w])",
        text,
    )

    return [
        round(
            float(value.replace(",", "")),
            2,
        )
        for value in matches
    ]


def collect_evidence_numbers(
    value: Any,
) -> list[float]:
    """Recursively collect numeric values from trusted evidence."""

    numbers = []

    if isinstance(value, bool):
        return numbers

    if isinstance(value, (int, float)):
        numbers.append(
            round(float(value), 2)
        )

    elif isinstance(value, dict):
        for item in value.values():
            numbers.extend(
                collect_evidence_numbers(item)
            )

    elif isinstance(value, list):
        for item in value:
            numbers.extend(
                collect_evidence_numbers(item)
            )

    return numbers


def validate_numeric_grounding(
    answer: str,
    evidence: Any,
) -> dict:
    """Check whether quantitative claims are supported by evidence."""

    answer_numbers = extract_business_numbers(
        answer
    )

    evidence_numbers = set(
        collect_evidence_numbers(
            evidence
        )
    )

    unsupported = [
        number
        for number in answer_numbers
        if number not in evidence_numbers
    ]

    supported_count = (
        len(answer_numbers)
        - len(unsupported)
    )

    rate = (
        supported_count
        / len(answer_numbers)
        * 100
        if answer_numbers
        else 100.0
    )

    return {
        "grounded": len(unsupported) == 0,
        "numbers_checked": len(answer_numbers),
        "supported_numbers": supported_count,
        "unsupported_numbers": unsupported,
        "numeric_faithfulness_rate": round(
            float(rate),
            2,
        ),
    }

class GroundingError(ValueError):
    """Raised when an answer contains unsupported quantitative claims."""


def require_numeric_grounding(
    answer: str,
    evidence: Any,
) -> dict:
    """Require every quantitative claim to be supported by evidence."""

    result = validate_numeric_grounding(
        answer,
        evidence,
    )

    if not result["grounded"]:
        unsupported = result[
            "unsupported_numbers"
        ]

        raise GroundingError(
            "Answer contains unsupported "
            f"quantitative claims: {unsupported}"
        )

    return result