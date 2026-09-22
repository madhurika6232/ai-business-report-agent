import pytest

from src.tools.ml_tools import (
    anomaly_detection_tool,
    delivery_risk_summary_tool,
)


def test_anomaly_detection_tool():
    result = anomaly_detection_tool(
        metric="late_rate",
        higher_is_bad=True,
    )

    assert len(result) == 4

    assert all(
        row["is_anomaly"] is True
        for row in result
    )

    assert all(
        row["impact"] in {
            "positive",
            "negative",
            "normal",
        }
        for row in result
    )

    assert all(
        row["severity"] in {
            "normal",
            "warning",
            "critical",
        }
        for row in result
    )


def test_delivery_risk_tool():
    result = delivery_risk_summary_tool(
        top_n=5,
    )

    assert len(result) == 5

    assert all(
        0 <= row["late_risk_probability"] <= 1
        for row in result
    )

    assert all(
        row["risk_level"] in {
            "low",
            "medium",
            "high",
            "critical",
        }
        for row in result
    )


def test_delivery_risk_ordering():
    result = delivery_risk_summary_tool(
        top_n=10,
    )

    probabilities = [
        row["late_risk_probability"]
        for row in result
    ]

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )


def test_invalid_delivery_risk_top_n():
    with pytest.raises(ValueError):
        delivery_risk_summary_tool(
            top_n=0,
        )


def test_invalid_anomaly_metric():
    with pytest.raises(ValueError):
        anomaly_detection_tool(
            metric="fake_metric",
        )