import pytest

from src.guardrails.pii import (
    detect_pii,
    redact_pii,
)


def test_normal_text_has_no_pii():
    result = detect_pii(
        "Customer reported that the product arrived late."
    )

    assert result.detected is False
    assert result.types == ()


def test_email_detected():
    result = detect_pii(
        "Contact maria@example.com regarding the order."
    )

    assert result.detected is True
    assert "email" in result.types


def test_phone_detected():
    result = detect_pii(
        "Call +1 415-555-1234 regarding the order."
    )

    assert result.detected is True
    assert "phone" in result.types


def test_credit_card_detected():
    result = detect_pii(
        "Card number 4111 1111 1111 1111 was mentioned."
    )

    assert result.detected is True
    assert "credit_card" in result.types


def test_email_redacted():
    result = redact_pii(
        "Contact maria@example.com."
    )

    assert result == (
        "Contact [REDACTED_EMAIL]."
    )


def test_phone_redacted():
    result = redact_pii(
        "Call +1 415-555-1234."
    )

    assert result == (
        "Call [REDACTED_PHONE]."
    )


def test_credit_card_redacted_before_phone():
    result = redact_pii(
        "Card number 4111 1111 1111 1111 was mentioned."
    )

    assert (
        "[REDACTED_PAYMENT_CARD]"
        in result
    )

    assert (
        "[REDACTED_PHONE]"
        not in result
    )

    assert (
        "4111"
        not in result
    )


def test_multiple_pii_redacted():
    result = redact_pii(
        "Contact maria@example.com or +1 415-555-1234."
    )

    assert (
        "[REDACTED_EMAIL]"
        in result
    )

    assert (
        "[REDACTED_PHONE]"
        in result
    )

    assert (
        "maria@example.com"
        not in result
    )


def test_non_string_detection_rejected():
    with pytest.raises(
        TypeError,
        match="text must be a string",
    ):
        detect_pii(123)


def test_non_string_redaction_rejected():
    with pytest.raises(
        TypeError,
        match="text must be a string",
    ):
        redact_pii(123)