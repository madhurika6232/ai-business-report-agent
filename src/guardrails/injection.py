import re

from dataclasses import dataclass


@dataclass(frozen=True)
class InjectionCheck:
    """Result of a prompt-injection check."""

    detected: bool
    risk_level: str
    matched_patterns: tuple[str, ...]


INJECTION_PATTERNS = {
    "ignore_instructions": (
        r"\bignore\s+(?:all\s+|any\s+)?"
        r"(?:previous|prior|above|system)\s+instructions?\b"
    ),

    "override_system": (
        r"\b(?:override|bypass|disregard)\s+"
        r"(?:the\s+)?(?:system|developer|safety|security)"
        r"(?:\s+instructions?|\s+rules?|\s+prompt)?\b"
    ),

    "reveal_prompt": (
        r"\b(?:reveal|show|print|display|repeat)\s+"
        r"(?:the\s+|your\s+)?"
        r"(?:system|developer|hidden)\s+"
        r"(?:prompt|instructions?|message)\b"
    ),

    "role_manipulation": (
        r"\b(?:act|pretend|behave)\s+as\s+"
        r"(?:if\s+you\s+are\s+)?"
        r"(?:the\s+)?(?:system|developer|administrator|admin)\b"
    ),

    "tool_bypass": (
        r"\b(?:bypass|ignore|disable)\s+"
        r"(?:the\s+)?"
        r"(?:tool|authorization|permission|guardrail|safety)"
        r"(?:s|\s+checks?|\s+rules?)?\b"
    ),
}


def detect_prompt_injection(
    text: str,
) -> InjectionCheck:
    """Detect common prompt-injection patterns."""

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string."
        )

    matched = []

    for name, pattern in INJECTION_PATTERNS.items():
        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            matched.append(
                name
            )

    if not matched:
        return InjectionCheck(
            detected=False,
            risk_level="none",
            matched_patterns=(),
        )

    risk_level = (
        "high"
        if len(matched) >= 2
        else "medium"
    )

    return InjectionCheck(
        detected=True,
        risk_level=risk_level,
        matched_patterns=tuple(matched),
    )


def evaluate_injection_dataset(
    dataset,
) -> tuple:
    """Evaluate prompt-injection detection against labeled examples."""

    results = []

    for _, row in dataset.iterrows():

        check = detect_prompt_injection(
            row["text"]
        )

        expected = str(
            row["expected_injection"]
        ).lower() == "true"

        results.append({
            "text": row["text"],
            "expected": expected,
            "predicted": check.detected,
            "correct": (
                expected == check.detected
            ),
            "risk_level": check.risk_level,
            "matched_patterns": (
                check.matched_patterns
            ),
        })

    import pandas as pd

    result_df = pd.DataFrame(
        results
    )

    metrics = {
        "total_examples": len(result_df),
        "accuracy": round(
            float(
                result_df["correct"].mean()
            ) * 100,
            2,
        ),
        "false_positives": int(
            (
                (~result_df["expected"])
                & result_df["predicted"]
            ).sum()
        ),
        "false_negatives": int(
            (
                result_df["expected"]
                & (~result_df["predicted"])
            ).sum()
        ),
    }

    return result_df, metrics