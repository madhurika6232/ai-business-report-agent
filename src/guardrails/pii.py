import re

from dataclasses import dataclass


@dataclass(frozen=True)
class PIICheck:
    """Result of PII detection."""

    detected: bool
    types: tuple[str, ...]


PII_PATTERNS = {
    "email": (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "phone": (
        r"(?<!\d)"
        r"(?:\+?\d{1,3}[\s.-]?)?"
        r"(?:\(?\d{2,3}\)?[\s.-]?)?"
        r"\d{3,4}[\s.-]\d{4}"
        r"(?!\d)"
    ),

    "credit_card": (
        r"\b(?:\d[ -]*?){13,19}\b"
    ),
}


def detect_pii(
    text: str,
) -> PIICheck:
    """Detect common PII patterns in text."""

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string."
        )

    detected_types = []

    for pii_type, pattern in PII_PATTERNS.items():

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            detected_types.append(
                pii_type
            )

    return PIICheck(
        detected=bool(detected_types),
        types=tuple(detected_types),
    )


def redact_pii(
    text: str,
) -> str:
    """Redact common PII before LLM or logging use."""

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string."
        )

    redacted = text

    # Order matters:
    # redact payment-card patterns before phone
    # patterns because their numeric formats can overlap.
    redaction_order = [
        (
            "credit_card",
            "[REDACTED_PAYMENT_CARD]",
        ),
        (
            "email",
            "[REDACTED_EMAIL]",
        ),
        (
            "phone",
            "[REDACTED_PHONE]",
        ),
    ]

    for pii_type, replacement in redaction_order:

        redacted = re.sub(
            PII_PATTERNS[pii_type],
            replacement,
            redacted,
            flags=re.IGNORECASE,
        )

    return redacted

def evaluate_pii_dataset(
    dataset,
) -> tuple:
    """Evaluate PII detection against labeled examples."""

    results = []

    for _, row in dataset.iterrows():

        check = detect_pii(
            row["text"]
        )

        expected = str(
            row["expected_pii"]
        ).lower() == "true"

        results.append({
            "text": row["text"],
            "expected": expected,
            "predicted": check.detected,
            "correct": (
                expected == check.detected
            ),
            "detected_types": check.types,
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