from src.tools.review_intelligence_tools import (
    complaint_themes_tool,
    delivery_complaint_evidence_tool,
)


def test_complaint_themes_tool():
    result = complaint_themes_tool(
        negative_only=True
    )

    assert len(result) > 0

    total_percentage = sum(
        row["percentage"]
        for row in result
    )

    assert abs(
        total_percentage - 100
    ) < 0.01


def test_top_negative_theme():
    result = complaint_themes_tool(
        negative_only=True
    )

    assert (
        result[0]["primary_issue"]
        == "non_delivery"
    )


def test_delivery_evidence_tool():
    result = (
        delivery_complaint_evidence_tool()
    )

    assert (
        result["delivery_related_complaints"]
        == 23
    )

    assert (
        result["delivery_delay_complaints"]
        == 10
    )

    assert (
        result["non_delivery_complaints"]
        == 13
    )

    assert (
        result["confirmed_late_deliveries"]
        == 4
    )

    assert (
        result["delay_confirmation_rate"]
        == 40.0
    )


def test_delivery_evidence_validity():
    result = (
        delivery_complaint_evidence_tool()
    )

    assert (
        0
        <= result["delay_confirmation_rate"]
        <= 100
    )