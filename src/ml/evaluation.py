import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


# ============================================================
# FORECASTING EVALUATION
# ============================================================

def calculate_forecast_metrics(
    actual,
    predicted,
) -> dict:
    """Calculate standard forecasting evaluation metrics."""

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted must have the same length."
        )

    mae = np.mean(
        np.abs(actual - predicted)
    )

    rmse = np.sqrt(
        np.mean((actual - predicted) ** 2)
    )

    non_zero = actual != 0

    mape = np.mean(
        np.abs(
            (actual[non_zero] - predicted[non_zero])
            / actual[non_zero]
        )
    ) * 100

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2),
    }


def compare_forecast_models(
    baseline_metrics: dict,
    candidate_metrics: dict,
) -> dict:
    """Compare forecasting models using MAPE."""

    baseline_mape = baseline_metrics["mape"]
    candidate_mape = candidate_metrics["mape"]

    if candidate_mape < baseline_mape:
        winner = "candidate"
    else:
        winner = "baseline"

    improvement_pct = (
        (baseline_mape - candidate_mape)
        / baseline_mape
        * 100
    )

    return {
        "winner": winner,
        "baseline_mape": baseline_mape,
        "candidate_mape": candidate_mape,
        "candidate_improvement_pct": round(
            float(improvement_pct),
            2,
        ),
    }


# ============================================================
# CLASSIFICATION EVALUATION
# ============================================================

def calculate_classification_metrics(
    actual,
    predicted,
    probabilities=None,
) -> dict:
    """Calculate binary classification metrics."""

    metrics = {
        "accuracy": round(
            float(
                accuracy_score(
                    actual,
                    predicted,
                )
            ),
            4,
        ),

        "precision": round(
            float(
                precision_score(
                    actual,
                    predicted,
                    zero_division=0,
                )
            ),
            4,
        ),

        "recall": round(
            float(
                recall_score(
                    actual,
                    predicted,
                    zero_division=0,
                )
            ),
            4,
        ),

        "f1": round(
            float(
                f1_score(
                    actual,
                    predicted,
                    zero_division=0,
                )
            ),
            4,
        ),
    }

    if probabilities is not None:
        metrics["roc_auc"] = round(
            float(
                roc_auc_score(
                    actual,
                    probabilities,
                )
            ),
            4,
        )

    return metrics


# ============================================================
# THRESHOLD EVALUATION
# ============================================================

def evaluate_thresholds(
    actual,
    probabilities,
    thresholds=None,
) -> pd.DataFrame:
    """
    Evaluate classification performance across
    probability thresholds.
    """

    if thresholds is None:
        thresholds = [
            0.30,
            0.40,
            0.50,
            0.60,
            0.70,
        ]

    results = []

    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            actual,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            actual,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            actual,
            predictions,
            zero_division=0,
        )

        results.append({
            "threshold": threshold,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "predicted_late": int(
                predictions.sum()
            ),
        })

    return pd.DataFrame(results)