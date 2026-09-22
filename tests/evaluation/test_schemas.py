import pytest
from pydantic import ValidationError

from src.evaluation.schemas import (
    EvaluationMetric,
    EvaluationResult,
    EvaluationSuiteResult,
)


def test_evaluation_metric():
    metric = EvaluationMetric(
        name="accuracy",
        value=100.0,
        threshold=95.0,
        status="pass",
    )

    assert metric.name == "accuracy"
    assert metric.value == 100.0
    assert metric.status == "pass"


def test_evaluation_result():
    metric = EvaluationMetric(
        name="accuracy",
        value=100.0,
        status="pass",
    )

    result = EvaluationResult(
        evaluator="router",
        category="routing",
        metrics=[metric],
        passed=True,
        sample_size=20,
    )

    assert result.evaluator == "router"
    assert result.passed is True
    assert result.sample_size == 20


def test_suite_score_bounds():
    with pytest.raises(
        ValidationError
    ):
        EvaluationSuiteResult(
            results=[],
            overall_score=120.0,
            passed=True,
            total_evaluators=0,
        )


def test_negative_sample_size_rejected():
    with pytest.raises(
        ValidationError
    ):
        EvaluationResult(
            evaluator="test",
            category="test",
            metrics=[],
            passed=False,
            sample_size=-1,
        )


def test_invalid_metric_status_rejected():
    with pytest.raises(
        ValidationError
    ):
        EvaluationMetric(
            name="accuracy",
            value=100.0,
            status="invalid",
        )