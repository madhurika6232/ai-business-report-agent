import pytest

from src.guardrails.grounding import (
    GroundingError,
    extract_business_numbers,
    validate_numeric_grounding,
    require_numeric_grounding,
)


def test_fully_grounded_answer():
    evidence = {
        "total_orders": 99092,
        "late_rate": 8.13,
    }

    result = validate_numeric_grounding(
        "There were 99092 orders with an 8.13% late rate.",
        evidence,
    )

    assert result["grounded"] is True
    assert result["numeric_faithfulness_rate"] == 100.0
    assert result["unsupported_numbers"] == []


def test_unsupported_number_detected():
    evidence = {
        "total_orders": 99092,
        "late_rate": 8.13,
    }

    result = validate_numeric_grounding(
        "There were 99092 orders with a 25.5% late rate.",
        evidence,
    )

    assert result["grounded"] is False

    assert result["unsupported_numbers"] == [
        25.5
    ]

    assert (
        result["numeric_faithfulness_rate"]
        == 50.0
    )


def test_grounding_error_raised():
    evidence = {
        "late_rate": 8.13,
    }

    with pytest.raises(
        GroundingError,
        match="unsupported quantitative claims",
    ):
        require_numeric_grounding(
            "The late rate was 25.5%.",
            evidence,
        )


def test_grounded_answer_allowed():
    evidence = {
        "late_rate": 8.13,
    }

    result = require_numeric_grounding(
        "The late rate was 8.13%.",
        evidence,
    )

    assert result["grounded"] is True


def test_dates_are_ignored():
    numbers = extract_business_numbers(
        "The late rate in 2018-03 was 21.36%."
    )

    assert numbers == [
        21.36
    ]


def test_delay_ranges_are_ignored():
    numbers = extract_business_numbers(
        (
            "Orders 4-7 days late had a 61.25% "
            "negative review rate."
        )
    )

    assert numbers == [
        61.25
    ]


def test_unicode_delay_ranges_are_ignored():
    numbers = extract_business_numbers(
        (
            "Orders 8–14 days late had a 78.1% "
            "negative review rate."
        )
    )

    assert numbers == [
        78.1
    ]


def test_plus_day_labels_are_ignored():
    numbers = extract_business_numbers(
        (
            "Orders 15+ days late had a 78.76% "
            "negative review rate."
        )
    )

    assert numbers == [
        78.76
    ]


def test_numbered_lists_are_ignored():
    numbers = extract_business_numbers(
        (
            "1. Revenue was 100.50.\n"
            "2. Late rate was 8.13%."
        )
    )

    assert numbers == [
        100.5,
        8.13,
    ]


def test_answer_without_numbers_is_grounded():
    result = validate_numeric_grounding(
        "Late deliveries are associated with lower review scores.",
        {},
    )

    assert result["grounded"] is True
    assert result["numbers_checked"] == 0
    assert result["numeric_faithfulness_rate"] == 100.0