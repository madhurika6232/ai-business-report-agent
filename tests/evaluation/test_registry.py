def test_evaluation_failure_is_captured(
    monkeypatch,
):
    from src.evaluation.runner import (
        evaluation_registry,
        run_evaluation_suite,
    )

    from src.evaluation.registry import (
        Evaluator,
    )

    def failing_evaluator():
        raise RuntimeError(
            "Simulated evaluation failure"
        )

    test_name = "test_failing_evaluator"

    monkeypatch.setitem(
        evaluation_registry._evaluators,
        test_name,
        Evaluator(
            name=test_name,
            category="test",
            description="Simulated failure.",
            handler=failing_evaluator,
        ),
    )

    scorecard = run_evaluation_suite([
        test_name
    ])

    result = scorecard[
        "suite"
    ].results[0]

    assert result.passed is False

    assert (
        result.metadata[
            "execution_failed"
        ]
        is True
    )

    assert (
        result.metrics[0].name
        == "evaluation_execution"
    )

    assert (
        result.metrics[0]
        .details["error_type"]
        == "RuntimeError"
    )

def test_incomplete_scorecard_cannot_be_saved_as_baseline(
    tmp_path,
    monkeypatch,
):
    from src.evaluation import regression

    from src.evaluation.runner import (
        save_scorecard_baseline,
    )

    from src.evaluation.schemas import (
        EvaluationMetric,
        EvaluationResult,
    )

    from src.evaluation.scorecard import (
        build_quality_scorecard,
    )

    monkeypatch.setattr(
        regression,
        "BASELINE_DIR",
        tmp_path,
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
        incomplete
    ])

    import pytest

    with pytest.raises(
        ValueError,
        match="Cannot save an incomplete evaluation",
    ):
        save_scorecard_baseline(
            scorecard=scorecard,
            name="invalid_baseline",
        )