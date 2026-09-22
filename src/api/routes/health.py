from fastapi import APIRouter

from src.api.config import (
    validate_production_config,
)


router = APIRouter(
    tags=["health"],
)


@router.get(
    "/health",
    summary="Service health",
)
def health_check() -> dict:
    """Return basic process health."""

    return {
        "status": "ok",
        "service": "RetailOps AI",
    }


@router.get(
    "/ready",
    summary="Service readiness",
)
def readiness_check() -> dict:
    """Return whether the application is ready to serve traffic."""

    validate_production_config()

    return {
        "status": "ready",
        "service": "RetailOps AI",
    }