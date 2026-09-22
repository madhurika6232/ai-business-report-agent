from src.tools.registry import (
    TOOL_REGISTRY,
    TOOL_DESCRIPTIONS,
)


def test_registry_is_complete():
    assert len(TOOL_REGISTRY) == 13
    assert len(TOOL_DESCRIPTIONS) == 13

    assert set(TOOL_REGISTRY) == set(
        TOOL_DESCRIPTIONS
    )


def test_business_question_tools():
    summary = TOOL_REGISTRY[
        "business_summary"
    ]()

    assert summary["total_orders"] == 99092
    assert summary["total_revenue"] > 0


def test_delivery_question_tools():
    delivery = TOOL_REGISTRY[
        "delivery_summary"
    ]()

    assert delivery["late_orders"] == 7823
    assert 0 <= delivery["late_rate"] <= 100


def test_customer_question_tools():
    reviews = TOOL_REGISTRY[
        "review_summary"
    ]()

    assert reviews["total_reviews"] == 98330
    assert 1 <= reviews["avg_review_score"] <= 5


def test_diagnostic_question_tools():
    delivery = TOOL_REGISTRY[
        "delivery_review_impact"
    ]()

    assert len(delivery) == 2

    statuses = {
        row["delivery_status"]
        for row in delivery
    }

    assert statuses == {
        "On time",
        "Late",
    }


def test_filtered_business_question():
    result = TOOL_REGISTRY[
        "business_summary"
    ](
        start_date="2018-01-01",
        end_date="2018-03-31 23:59:59",
        customer_state="SP",
        category="furniture_decor",
    )

    assert result["total_orders"] == 515
    assert result["total_revenue"] > 0