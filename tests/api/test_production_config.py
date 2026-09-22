import importlib

import pytest

import src.api.config as config


def reload_config(
    monkeypatch,
    **environment,
):
    keys = [
        "RETAILOPS_ENV",
        "GROQ_API_KEY",
        "RETAILOPS_API_KEY",
        "RETAILOPS_API_DEBUG",
        "RETAILOPS_CORS_ORIGINS",
        "RETAILOPS_API_DOCS_ENABLED",
    ]

    for key in keys:
        monkeypatch.delenv(
            key,
            raising=False,
        )

    for key, value in environment.items():
        monkeypatch.setenv(
            key,
            value,
        )

    return importlib.reload(
        config
    )


def test_development_config_allows_missing_secrets(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="development",
    )

    loaded.validate_production_config()


def test_testing_config_allows_missing_secrets(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="testing",
    )

    loaded.validate_production_config()


def test_production_requires_groq_key(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
    )

    with pytest.raises(
        ValueError,
        match="GROQ_API_KEY is required",
    ):
        loaded.validate_production_config()


def test_production_requires_api_key(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="real-groq-key",
    )

    with pytest.raises(
        ValueError,
        match="RETAILOPS_API_KEY is required",
    ):
        loaded.validate_production_config()


def test_production_rejects_placeholders(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="your-groq-api-key-here",
        RETAILOPS_API_KEY="real-api-key",
    )

    with pytest.raises(
        ValueError,
        match="placeholder",
    ):
        loaded.validate_production_config()


def test_production_rejects_debug(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="real-groq-key",
        RETAILOPS_API_KEY="real-api-key",
        RETAILOPS_API_DEBUG="true",
        RETAILOPS_CORS_ORIGINS=(
            "https://app.example.com"
        ),
    )

    with pytest.raises(
        ValueError,
        match="DEBUG",
    ):
        loaded.validate_production_config()


def test_production_accepts_valid_configuration(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="real-groq-key",
        RETAILOPS_API_KEY="real-api-key",
        RETAILOPS_API_DEBUG="false",
        RETAILOPS_API_DOCS_ENABLED="false",
        RETAILOPS_CORS_ORIGINS=(
            "https://app.example.com"
        ),
    )

    loaded.validate_production_config()


def test_invalid_environment_rejected(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="staging",
    )

    with pytest.raises(
        ValueError,
        match="RETAILOPS_ENV",
    ):
        loaded.validate_production_config()

def test_production_rejects_enabled_docs(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="real-groq-key",
        RETAILOPS_API_KEY="real-api-key",
        RETAILOPS_API_DEBUG="false",
        RETAILOPS_API_DOCS_ENABLED="true",
        RETAILOPS_CORS_ORIGINS=(
            "https://app.example.com"
        ),
    )

    with pytest.raises(
        ValueError,
        match="DOCS_ENABLED",
    ):
        loaded.validate_production_config()


def test_production_accepts_disabled_docs(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_ENV="production",
        GROQ_API_KEY="real-groq-key",
        RETAILOPS_API_KEY="real-api-key",
        RETAILOPS_API_DEBUG="false",
        RETAILOPS_API_DOCS_ENABLED="false",
        RETAILOPS_CORS_ORIGINS=(
            "https://app.example.com"
        ),
    )

    loaded.validate_production_config()