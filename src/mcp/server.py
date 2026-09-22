from typing import Any

from mcp.server import MCPServer

from src.skills import retailops_skills
from src.mcp.resources import (
    get_platform_info,
    get_skill_catalog,
    get_domain_catalog,
)


# ============================================================
# MCP SERVER
# ============================================================

mcp = MCPServer(
    "RetailOps AI",
    description=(
        "Retail operations analytics, customer intelligence, "
        "and risk capabilities."
    ),
)


# ============================================================
# MCP RESOURCES
# ============================================================

@mcp.resource("retailops://platform")
def platform_resource() -> dict[str, Any]:
    """Return RetailOps AI platform metadata."""

    return get_platform_info()


@mcp.resource("retailops://skills")
def skills_resource() -> list[dict[str, str]]:
    """Return the RetailOps skill catalog."""

    return get_skill_catalog()


@mcp.resource("retailops://domains")
def domains_resource() -> dict[str, list[str]]:
    """Return RetailOps skills grouped by domain."""

    return get_domain_catalog()


# ============================================================
# MCP TOOLS
# ============================================================

@mcp.tool()
def business_summary() -> dict:
    """Return core marketplace business KPIs."""

    return retailops_skills.execute(
        "business_summary"
    )


@mcp.tool()
def delivery_summary() -> dict:
    """Return overall marketplace delivery performance."""

    return retailops_skills.execute(
        "delivery_summary"
    )


@mcp.tool()
def cancellation_metrics() -> dict:
    """Return marketplace cancellation metrics."""

    return retailops_skills.execute(
        "cancellation_metrics"
    )


@mcp.tool()
def complaint_themes(
    negative_only: bool = True,
) -> list[dict]:
    """Return classified customer complaint themes."""

    return retailops_skills.execute(
        "complaint_themes",
        negative_only=negative_only,
    )


@mcp.tool()
def delivery_anomalies() -> list[dict]:
    """Return detected late-delivery anomalies."""

    return retailops_skills.execute(
        "delivery_anomaly_detection",
        metric="late_rate",
        higher_is_bad=True,
    )


@mcp.tool()
def delivery_risk(
    top_n: int = 10,
) -> list[dict]:
    """Return orders with the highest late-delivery risk scores."""

    return retailops_skills.execute(
        "delivery_risk_screening",
        top_n=top_n,
    )


@mcp.tool()
def forecast_method() -> dict:
    """Return the validated revenue forecasting approach."""

    return retailops_skills.execute(
        "forecast_method"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )