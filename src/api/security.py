import os
import secrets

from fastapi import (
    Header,
    HTTPException,
    status,
)


API_KEY_ENV = "RETAILOPS_API_KEY"


def get_configured_api_key() -> str | None:
    """Return the configured RetailOps API key."""

    value = os.getenv(
        API_KEY_ENV
    )

    if value is None:
        return None

    value = value.strip()

    return value or None


def require_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> None:
    """Require a valid API key when API security is configured."""

    configured_key = (
        get_configured_api_key()
    )

    # Development mode:
    # no configured key means authentication is disabled.
    if configured_key is None:
        return

    if (
        x_api_key is None
        or not secrets.compare_digest(
            x_api_key,
            configured_key,
        )
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="Invalid or missing API key.",
        )