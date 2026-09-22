import importlib

import src.api.config as config


def reload_config(
    monkeypatch,
    **environment,
):
    keys = [
        "RETAILOPS_API_TITLE",
        "RETAILOPS_API_VERSION",
        "RETAILOPS_API_DEBUG",
        "RETAILOPS_CORS_ORIGINS",
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


def test_default_configuration(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch
    )

    assert (
        loaded.API_TITLE
        == "RetailOps AI API"
    )

    assert (
        loaded.API_VERSION
        == "1.0.0"
    )

    assert loaded.API_DEBUG is False

    assert loaded.CORS_ORIGINS == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",

    ]


def test_custom_api_configuration(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_API_TITLE=(
            "RetailOps Production API"
        ),
        RETAILOPS_API_VERSION="2.0.0",
        RETAILOPS_API_DEBUG="true",
    )

    assert (
        loaded.API_TITLE
        == "RetailOps Production API"
    )

    assert (
        loaded.API_VERSION
        == "2.0.0"
    )

    assert loaded.API_DEBUG is True


def test_custom_cors_origins(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_CORS_ORIGINS=(
            "https://app.example.com,"
            "https://admin.example.com"
        ),
    )

    assert loaded.CORS_ORIGINS == [
        "https://app.example.com",
        "https://admin.example.com",
    ]


def test_boolean_false_values(
    monkeypatch,
):
    loaded = reload_config(
        monkeypatch,
        RETAILOPS_API_DEBUG="false",
    )

    assert loaded.API_DEBUG is False