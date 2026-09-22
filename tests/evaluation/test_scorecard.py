import pytest

from src.evaluation.schemas import (
    EvaluationMetric,
    EvaluationResult,
)

from src.evaluation.scorecard import (
    build_quality_scorecard,
)


def make_result(
    evaluator,
    value,
    passed=True,
    status="pass",
):
    return EvaluationResult(
        evaluator=evaluator,
        category="test",
        metrics=[
            EvaluationMetric(
                name="test_metric",
                value=value,
                status=status,
            )
        ],
        passed=passed,
        sample_size=10,
    )


def test_all_pass_produces_pass():
    results = [
        make_result(
            "router",
            100.0,
        ),
        make_result(
            "guardrails",
            100.0,
        ),
    ]

    scorecard = build_quality_scorecard(
        results
    )

    assert (
        scorecard["release_decision"]
        == "pass"
    )

    assert (
        scorecard["suite"].passed
        is True
    )


def test_critical_failure_produces_fail():
    results = [
        make_result(
            "router",
            100.0,
        ),
        make_result(
            "guardrails",
            90.0,
            passed=False,
            status="fail",
        ),
    ]

    scorecard = build_quality_scorecard(
        results
    )

    assert (
        scorecard["release_decision"]
        == "fail"
    )

    assert "guardrails" in (
        scorecard[
            "critical_failures"
        ]
    )

    assert (
        scorecard["suite"].passed
        is False
    )


def test_noncritical_failure_produces_warning():
    results = [
        make_result(
            "router",
            100.0,
        ),
        make_result(
            "answer_quality",
            3.5,
            passed=False,
            status="fail",
        ),
    ]

    scorecard = build_quality_scorecard(
        results
    )

    assert (
        scorecard["release_decision"]
        == "warning"
    )

    assert "answer_quality" in (
        scorecard[
            "noncritical_failures"
        ]
    )


def test_answer_quality_normalized():
    result = EvaluationResult(
        evaluator="answer_quality",
        category="answer_quality",
        metrics=[
            EvaluationMetric(
                name="overall_answer_quality",
                value=4.5,
                threshold=4.0,
                status="pass",
            )
        ],
        passed=True,
        sample_size=5,
    )

    scorecard = build_quality_scorecard([
        result
    ])

    assert (
        scorecard[
            "evaluator_scores"
        ]["answer_quality"]
        == pytest.approx(90.0)
    )


def test_empty_results_rejected():
    with pytest.raises(
        ValueError,
        match="At least one evaluation result",
    ):
        build_quality_scorecard([])


def test_incomplete_evaluator_produces_incomplete_decision():
    completed = make_result(
        "guardrails",
        100.0,
    )

    incomplete = EvaluationResult(
        evaluator="numeric_grounding",
        category="grounding",
        metrics=[
            EvaluationMetric(
                name="evaluation_execution",
                value=0.0,
                status="fail",
                details={
                    "error_type": "RateLimitError",
                },
            )
        ],
        passed=False,
        completed=False,
        sample_size=0,
    )

    scorecard = build_quality_scorecard([
        completed,
        incomplete,
    ])

    assert (
        scorecard["release_decision"]
        == "incomplete"
    )

    assert (
        scorecard[
            "evaluator_scores"
        ]["numeric_grounding"]
        is None
    )

    assert (
        scorecard[
            "incomplete_evaluators"
        ]
        == ["numeric_grounding"]
    )

    assert (
        scorecard[
            "critical_failures"
        ]
        == []
    )


def test_incomplete_evaluator_excluded_from_score():
    completed = make_result(
        "guardrails",
        100.0,
    )

    incomplete = EvaluationResult(
        evaluator="numeric_grounding",
        category="grounding",
        metrics=[
            EvaluationMetric(
                name="evaluation_execution",
                value=0.0,
                status="fail",
            )
        ],
        passed=False,
        completed=False,
        sample_size=0,
    )

    scorecard = build_quality_scorecard([
        completed,
        incomplete,
    ])

    assert (
        scorecard["suite"].overall_score
        == 100.0
    )