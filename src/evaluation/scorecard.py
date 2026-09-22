from typing import Literal

from src.evaluation.schemas import (
    EvaluationResult,
    EvaluationSuiteResult,
)

from src.evaluation.thresholds import (
    is_critical_evaluator,
)


ReleaseDecision = Literal[
    "pass",
    "warning",
    "fail",
    "incomplete",
]


# Weight each evaluation area in the overall score.
EVALUATOR_WEIGHTS = {
    "router": 0.15,
    "tool_selection": 0.10,
    "review_classifier": 0.15,
    "numeric_grounding": 0.20,
    "guardrails": 0.15,
    "multi_agent": 0.15,
    "answer_quality": 0.10,
}


def _normalize_evaluator_score(
    result: EvaluationResult,
) -> float:
    """Convert evaluator metrics into a normalized 0-100 score."""

    scores = []

    for metric in result.metrics:

        # Answer-quality metrics use a 1-5 scale.
        if result.evaluator == "answer_quality":
            score = (
                metric.value / 5.0 * 100
            )

        # Error/count metrics are best represented
        # by their pass/fail status.
        elif (
            "failure_rate" in metric.name
            or "false_positive" in metric.name
            or "false_negative" in metric.name
            or "unsupported" in metric.name
            or "unsafe_answers" in metric.name
        ):
            score = (
                100.0
                if metric.status == "pass"
                else 0.0
            )

        else:
            score = metric.value

        scores.append(
            max(
                0.0,
                min(100.0, float(score)),
            )
        )

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2,
    )


def build_quality_scorecard(
    results: list[EvaluationResult],
) -> dict:
    """Build the RetailOps evaluation scorecard."""

    if not results:
        raise ValueError(
            "At least one evaluation result is required."
        )

    evaluator_scores = {}

    weighted_score = 0.0
    total_weight = 0.0

    critical_failures = []
    noncritical_failures = []
    incomplete_evaluators = []

    for result in results:

        # ----------------------------------------
        # Incomplete evaluations
        # ----------------------------------------

        if not result.completed:

            evaluator_scores[
                result.evaluator
            ] = None

            incomplete_evaluators.append(
                result.evaluator
            )

            # Do not include unavailable
            # evaluations in the quality score.
            continue

        # ----------------------------------------
        # Completed evaluations
        # ----------------------------------------

        score = _normalize_evaluator_score(
            result
        )

        evaluator_scores[
            result.evaluator
        ] = score

        weight = EVALUATOR_WEIGHTS.get(
            result.evaluator,
            0.0,
        )

        weighted_score += (
            score * weight
        )

        total_weight += weight

        if not result.passed:

            if is_critical_evaluator(
                result.evaluator
            ):
                critical_failures.append(
                    result.evaluator
                )

            else:
                noncritical_failures.append(
                    result.evaluator
                )

    # ----------------------------------------
    # Overall quality score
    # ----------------------------------------

    overall_score = (
        weighted_score / total_weight
        if total_weight > 0
        else 0.0
    )

    overall_score = round(
        overall_score,
        2,
    )

    # ----------------------------------------
    # Release decision
    # ----------------------------------------

    if incomplete_evaluators:
        decision = "incomplete"

    elif critical_failures:
        decision = "fail"

    elif noncritical_failures:
        decision = "warning"

    else:
        decision = "pass"

    suite = EvaluationSuiteResult(
        results=results,
        overall_score=overall_score,
        passed=(
            decision == "pass"
        ),
        total_evaluators=len(
            results
        ),
    )

    return {
        "suite": suite,
        "evaluator_scores": evaluator_scores,
        "release_decision": decision,
        "critical_failures": critical_failures,
        "noncritical_failures": noncritical_failures,
        "incomplete_evaluators": incomplete_evaluators,
    }