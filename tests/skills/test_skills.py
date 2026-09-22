import pytest

from src.skills import (
    retailops_skills,
)

from src.skills.registry import (
    Skill,
    SkillRegistry,
)


def test_global_skill_count():
    assert len(
        retailops_skills
    ) == 19


def test_skill_domain_counts():
    assert len(
        retailops_skills.list_skills(
            domain="business"
        )
    ) == 4

    assert len(
        retailops_skills.list_skills(
            domain="operations"
        )
    ) == 5

    assert len(
        retailops_skills.list_skills(
            domain="customer"
        )
    ) == 6

    assert len(
        retailops_skills.list_skills(
            domain="risk"
        )
    ) == 4


def test_business_summary_skill():
    result = retailops_skills.execute(
        "business_summary"
    )

    assert result["total_orders"] == 99092

    assert (
        result["total_revenue"]
        == pytest.approx(
            13541712.78
        )
    )


def test_delivery_summary_skill():
    result = retailops_skills.execute(
        "delivery_summary"
    )

    assert (
        result["delivered_orders"]
        == 96204
    )

    assert (
        result["late_orders"]
        == 7823
    )

    assert (
        result["late_rate"]
        == pytest.approx(
            8.13
        )
    )


def test_review_summary_skill():
    result = retailops_skills.execute(
        "review_summary"
    )

    assert (
        1
        <= result["avg_review_score"]
        <= 5
    )


def test_anomaly_skill():
    result = retailops_skills.execute(
        "delivery_anomaly_detection",
        metric="late_rate",
        higher_is_bad=True,
    )

    assert len(result) == 4


def test_forecast_method_skill():
    result = retailops_skills.execute(
        "forecast_method"
    )

    assert (
        result["selected_model"]
        == "naive_baseline"
    )

    assert (
        result["holdout_mape"]
        == pytest.approx(
            4.94
        )
    )


def test_unknown_skill():
    with pytest.raises(
        KeyError,
        match="Unknown skill",
    ):
        retailops_skills.execute(
            "not_a_real_skill"
        )


def test_duplicate_skill_rejected():
    registry = SkillRegistry()

    skill = Skill(
        name="test",
        description="Test skill",
        domain="test",
        handler=lambda: {},
    )

    registry.register(
        skill
    )

    with pytest.raises(
        ValueError,
        match="Skill already registered",
    ):
        registry.register(
            skill
        )