import pytest

from src.evaluation import regression


@pytest.fixture
def temporary_baseline_dir(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        regression,
        "BASELINE_DIR",
        tmp_path,
    )

    return tmp_path


def test_save_and_load_baseline(
    temporary_baseline_dir,
):
    path = regression.save_baseline(
        name="test_baseline",
        evaluator_scores={
            "router": 100.0,
            "guardrails": 100.0,
        },
        overall_score=100.0,
        metadata={
            "version": "test",
        },
    )

    assert path.exists()

    baseline = regression.load_baseline(
        "test_baseline"
    )

    assert (
        baseline["name"]
        == "test_baseline"
    )

    assert (
        baseline["overall_score"]
        == 100.0
    )

    assert (
        baseline[
            "evaluator_scores"
        ]["router"]
        == 100.0
    )


def test_regression_detected():
    baseline = {
        "name": "baseline",
        "overall_score": 100.0,
        "evaluator_scores": {
            "router": 100.0,
            "guardrails": 100.0,
        },
    }

    result = regression.compare_with_baseline(
        current_scores={
            "router": 100.0,
            "guardrails": 95.0,
        },
        current_overall_score=97.5,
        baseline=baseline,
        tolerance=2.0,
    )

    assert (
        result["regression_detected"]
        is True
    )

    assert (
        "guardrails"
        in result["regressions"]
    )

    assert (
        result[
            "regressions"
        ]["guardrails"]["difference"]
        == -5.0
    )


def test_improvement_detected():
    baseline = {
        "name": "baseline",
        "overall_score": 95.0,
        "evaluator_scores": {
            "answer_quality": 90.0,
        },
    }

    result = regression.compare_with_baseline(
        current_scores={
            "answer_quality": 100.0,
        },
        current_overall_score=100.0,
        baseline=baseline,
        tolerance=2.0,
    )

    assert (
        result["regression_detected"]
        is False
    )

    assert (
        "answer_quality"
        in result["improvements"]
    )

    assert (
        result[
            "improvements"
        ]["answer_quality"]["difference"]
        == 10.0
    )


def test_change_within_tolerance_ignored():
    baseline = {
        "name": "baseline",
        "overall_score": 100.0,
        "evaluator_scores": {
            "router": 100.0,
        },
    }

    result = regression.compare_with_baseline(
        current_scores={
            "router": 99.0,
        },
        current_overall_score=99.0,
        baseline=baseline,
        tolerance=2.0,
    )

    assert (
        result["regression_detected"]
        is False
    )

    assert result["regressions"] == {}
    assert result["improvements"] == {}


def test_negative_tolerance_rejected():
    baseline = {
        "name": "baseline",
        "overall_score": 100.0,
        "evaluator_scores": {},
    }

    with pytest.raises(
        ValueError,
        match="tolerance cannot be negative",
    ):
        regression.compare_with_baseline(
            current_scores={},
            current_overall_score=100.0,
            baseline=baseline,
            tolerance=-1.0,
        )


def test_missing_baseline_rejected(
    temporary_baseline_dir,
):
    with pytest.raises(
        FileNotFoundError,
        match="Baseline not found",
    ):
        regression.load_baseline(
            "does_not_exist"
        )


def test_empty_baseline_name_rejected(
    temporary_baseline_dir,
):
    with pytest.raises(
        ValueError,
        match="Baseline name cannot be empty",
    ):
        regression.save_baseline(
            name="",
            evaluator_scores={},
            overall_score=100.0,
        )