from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_evaluation_status():
    response = client.get(
        "/api/v1/evaluation"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["evaluator_count"] == 7
    assert len(data["evaluators"]) == 7


def test_evaluation_names():
    response = client.get(
        "/api/v1/evaluation"
    )

    data = response.json()

    names = {
        evaluator["name"]
        for evaluator in data["evaluators"]
    }

    assert names == {
        "router",
        "tool_selection",
        "review_classifier",
        "numeric_grounding",
        "guardrails",
        "multi_agent",
        "answer_quality",
    }


def test_release_thresholds_exposed():
    response = client.get(
        "/api/v1/evaluation"
    )

    thresholds = response.json()[
        "thresholds"
    ]

    assert (
        thresholds[
            "router"
        ][
            "exact_route_accuracy"
        ]
        == 95.0
    )

    assert (
        thresholds[
            "numeric_grounding"
        ][
            "guardrail_containment_rate"
        ]
        == 100.0
    )

    assert (
        thresholds[
            "answer_quality"
        ][
            "overall_answer_quality"
        ]
        == 4.0
    )


def test_v1_baseline_available():
    response = client.get(
        "/api/v1/evaluation"
    )

    baseline = response.json()[
        "baseline"
    ]

    assert (
        baseline["name"]
        == "retailops_baseline_v1"
    )

    assert baseline[
        "available"
    ] is True

    assert (
        baseline["overall_score"]
        == 92.82
    )

    assert (
        baseline["release_decision"]
        == "pass"
    )


def test_evaluation_endpoint_does_not_run_suite(
    monkeypatch,
):
    """
    The status endpoint must never trigger the expensive
    evaluation suite.
    """

    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "Evaluation suite must not run "
            "from the status endpoint."
        )

    monkeypatch.setattr(
        "src.evaluation.runner.run_evaluation_suite",
        fail_if_called,
    )

    response = client.get(
        "/api/v1/evaluation"
    )

    assert response.status_code == 200