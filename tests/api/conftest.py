import pytest

from src.api.security import (
    API_KEY_ENV,
)


@pytest.fixture(
    autouse=True,
)
def isolate_api_key(
    monkeypatch,
):
    """
    Keep ordinary API tests independent from the
    developer or production RETAILOPS_API_KEY.

    Authentication-specific tests explicitly set
    the environment variable themselves.
    """

    monkeypatch.delenv(
        API_KEY_ENV,
        raising=False,
    )