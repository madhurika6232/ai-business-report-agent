from fastapi import APIRouter

from src.evaluation.runner import (
    evaluation_registry,
)

from src.evaluation.thresholds import (
    RELEASE_THRESHOLDS,
)

from src.evaluation.regression import (
    load_baseline,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["evaluation"],
)


@router.get(
    "/evaluation",
    summary="Get evaluation framework status",
)
def evaluation_status() -> dict:
    """Return evaluation configuration and baseline status."""

    evaluators = (
        evaluation_registry.list_evaluators()
    )

    baseline_name = (
        "retailops_baseline_v1"
    )

    try:
        baseline = load_baseline(
            baseline_name
        )

        baseline_available = True

    except FileNotFoundError:
        baseline = None
        baseline_available = False

    return {
        "evaluator_count": len(
            evaluators
        ),
        "evaluators": [
            {
                "name": evaluator.name,
                "category": evaluator.category,
                "description": evaluator.description,
            }
            for evaluator in evaluators
        ],
        "thresholds": RELEASE_THRESHOLDS,
        "baseline": {
            "name": baseline_name,
            "available": baseline_available,
            "overall_score": (
                baseline["overall_score"]
                if baseline is not None
                else None
            ),
            "release_decision": (
                baseline.get(
                    "metadata",
                    {},
                ).get(
                    "release_decision"
                )
                if baseline is not None
                else None
            ),
        },
    }