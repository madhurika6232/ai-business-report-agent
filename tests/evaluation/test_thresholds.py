import pytest

from src.evaluation.thresholds import (
    RELEASE_THRESHOLDS,
    get_threshold,
    is_critical_evaluator,
)


def test_seven_evaluators_configured():
    assert len(
        RELEASE_THRESHOLDS
    ) == 7


def test_router_threshold():
    assert get_threshold(
        "router",
        "exact_route_accuracy",
    ) == 95.0


def test_grounding_containment_threshold():
    assert get_threshold(
        "numeric_grounding",
        "guardrail_containment_rate",
    ) == 100.0


def test_answer_quality_threshold():
    assert get_threshold(
        "answer_quality",
        "overall_answer_quality",
    ) == 4.0


def test_guardrails_are_critical():
    assert is_critical_evaluator(
        "guardrails"
    ) is True


def test_grounding_is_critical():
    assert is_critical_evaluator(
        "numeric_grounding"
    ) is True


def test_answer_quality_not_critical():
    assert is_critical_evaluator(
        "answer_quality"
    ) is False


def test_unknown_evaluator_rejected():
    with pytest.raises(
        KeyError,
        match="Unknown evaluator",
    ):
        get_threshold(
            "unknown",
            "accuracy",
        )


def test_unknown_metric_rejected():
    with pytest.raises(
        KeyError,
        match="Unknown metric",
    ):
        get_threshold(
            "router",
            "not_a_metric",
        )