from src.skills.registry import (
    Skill,
    SkillRegistry,
)

from src.tools.ml_tools import (
    anomaly_detection_tool,
    delivery_risk_summary_tool,
)

from src.tools.business_tools import (
    monthly_performance_tool,
)


def forecast_method_skill() -> dict:
    """Return the validated forecasting approach."""

    return {
        "selected_model": "naive_baseline",
        "holdout_mape": 4.94,
        "note": (
            "The naive baseline outperformed "
            "Holt exponential smoothing on "
            "temporal holdout validation."
        ),
    }


def register_risk_skills(
    registry: SkillRegistry,
) -> None:
    """Register ML and risk-analysis skills."""

    registry.register(
        Skill(
            name="delivery_anomaly_detection",
            description=(
                "Detect unusual monthly late-delivery "
                "behavior using historical baselines."
            ),
            domain="risk",
            handler=anomaly_detection_tool,
        )
    )

    registry.register(
        Skill(
            name="delivery_risk_screening",
            description=(
                "Return orders with the highest model-estimated "
                "late-delivery risk scores."
            ),
            domain="risk",
            handler=delivery_risk_summary_tool,
        )
    )

    registry.register(
        Skill(
            name="forecast_history",
            description=(
                "Return monthly marketplace performance "
                "used for forecasting."
            ),
            domain="risk",
            handler=monthly_performance_tool,
        )
    )

    registry.register(
        Skill(
            name="forecast_method",
            description=(
                "Return the forecasting method selected "
                "through temporal model evaluation."
            ),
            domain="risk",
            handler=forecast_method_skill,
        )
    )