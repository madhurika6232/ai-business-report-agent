import time

import pandas as pd

from sklearn.metrics import (
    precision_recall_fscore_support,
)

from src.intelligence.review_classifier import (
    classify_review_safe,
)


# ============================================================
# EVALUATION PACING
# ============================================================

GROQ_EVALUATION_DELAY_SECONDS = 2.0


def _pace_groq_evaluation() -> None:
    """Pause between Groq-backed review-classification cases."""

    time.sleep(
        GROQ_EVALUATION_DELAY_SECONDS
    )


# ============================================================
# REVIEW CLASSIFIER EVALUATION
# ============================================================

def evaluate_review_classifier(
    golden_set: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Evaluate Groq review classification against labeled examples."""

    results = []

    for _, row in golden_set.iterrows():

        try:
            classification = classify_review_safe(
                row["review_text"],
                max_attempts=2,
            )

            sentiment_correct = (
                classification.sentiment
                == row["expected_sentiment"]
            )

            issue_correct = (
                classification.primary_issue
                == row["expected_primary_issue"]
            )

            results.append({
                "review_text": (
                    row["review_text"]
                ),
                "expected_sentiment": (
                    row["expected_sentiment"]
                ),
                "predicted_sentiment": (
                    classification.sentiment
                ),
                "sentiment_correct": (
                    sentiment_correct
                ),
                "expected_primary_issue": (
                    row[
                        "expected_primary_issue"
                    ]
                ),
                "predicted_primary_issue": (
                    classification.primary_issue
                ),
                "issue_correct": (
                    issue_correct
                ),
                "schema_valid": True,
                "failed": False,
            })

        except Exception:
            results.append({
                "review_text": (
                    row["review_text"]
                ),
                "expected_sentiment": (
                    row["expected_sentiment"]
                ),
                "predicted_sentiment": None,
                "sentiment_correct": False,
                "expected_primary_issue": (
                    row[
                        "expected_primary_issue"
                    ]
                ),
                "predicted_primary_issue": None,
                "issue_correct": False,
                "schema_valid": False,
                "failed": True,
            })

        # Pace every Groq-backed evaluation case,
        # including failed attempts.
        _pace_groq_evaluation()

    result_df = pd.DataFrame(
        results
    )

    total = len(
        result_df
    )

    metrics = {
        "total_examples": total,

        "sentiment_accuracy": round(
            float(
                result_df[
                    "sentiment_correct"
                ].mean()
            ) * 100,
            2,
        ),

        "issue_accuracy": round(
            float(
                result_df[
                    "issue_correct"
                ].mean()
            ) * 100,
            2,
        ),

        "schema_validity_rate": round(
            float(
                result_df[
                    "schema_valid"
                ].mean()
            ) * 100,
            2,
        ),

        "failure_rate": round(
            float(
                result_df[
                    "failed"
                ].mean()
            ) * 100,
            2,
        ),
    }

    successful = result_df[
        ~result_df["failed"]
    ].copy()

    if not successful.empty:

        precision, recall, f1, _ = (
            precision_recall_fscore_support(
                successful[
                    "expected_primary_issue"
                ],
                successful[
                    "predicted_primary_issue"
                ],
                average="macro",
                zero_division=0,
            )
        )

        metrics[
            "issue_macro_precision"
        ] = round(
            float(precision) * 100,
            2,
        )

        metrics[
            "issue_macro_recall"
        ] = round(
            float(recall) * 100,
            2,
        )

        metrics[
            "issue_macro_f1"
        ] = round(
            float(f1) * 100,
            2,
        )

    return result_df, metrics