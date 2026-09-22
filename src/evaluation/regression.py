import json
from pathlib import Path
from typing import Any


BASELINE_DIR = Path(
    "data/evaluation/baselines"
)


def save_baseline(
    name: str,
    evaluator_scores: dict[str, float],
    overall_score: float,
    metadata: dict[str, Any] | None = None,
) -> Path:
    """Save an evaluation baseline snapshot."""

    if not name or not name.strip():
        raise ValueError(
            "Baseline name cannot be empty."
        )

    BASELINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "name": name,
        "overall_score": float(
            overall_score
        ),
        "evaluator_scores": {
            key: float(value)
            for key, value
            in evaluator_scores.items()
        },
        "metadata": metadata or {},
    }

    path = (
        BASELINE_DIR
        / f"{name}.json"
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path


def load_baseline(
    name: str,
) -> dict:
    """Load a saved evaluation baseline."""

    path = (
        BASELINE_DIR
        / f"{name}.json"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline not found: {name}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def compare_with_baseline(
    current_scores: dict[str, float],
    current_overall_score: float,
    baseline: dict,
    tolerance: float = 2.0,
) -> dict:
    """Compare current evaluation scores with a baseline."""

    if tolerance < 0:
        raise ValueError(
            "tolerance cannot be negative."
        )

    baseline_scores = baseline[
        "evaluator_scores"
    ]

    regressions = {}
    improvements = {}

    all_evaluators = set(
        baseline_scores
    ) | set(
        current_scores
    )

    for evaluator in all_evaluators:

        if (
            evaluator not in baseline_scores
            or evaluator not in current_scores
        ):
            continue

        previous = float(
            baseline_scores[
                evaluator
            ]
        )

        current = float(
            current_scores[
                evaluator
            ]
        )

        difference = round(
            current - previous,
            2,
        )

        if difference < -tolerance:
            regressions[evaluator] = {
                "baseline": previous,
                "current": current,
                "difference": difference,
            }

        elif difference > tolerance:
            improvements[evaluator] = {
                "baseline": previous,
                "current": current,
                "difference": difference,
            }

    overall_difference = round(
        float(current_overall_score)
        - float(baseline["overall_score"]),
        2,
    )

    return {
        "baseline_name": baseline["name"],
        "overall_baseline": float(
            baseline["overall_score"]
        ),
        "overall_current": float(
            current_overall_score
        ),
        "overall_difference": overall_difference,
        "regressions": regressions,
        "improvements": improvements,
        "regression_detected": bool(
            regressions
        ),
    }