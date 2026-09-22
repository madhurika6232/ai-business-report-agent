import os


def _parse_bool(
    value: str | None,
    default: bool,
) -> bool:
    """Parse a boolean environment value."""

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _parse_origins(
    value: str | None,
) -> list[str]:
    """Parse comma-separated CORS origins."""

    if not value:
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]

    return [
        origin.strip()
        for origin in value.split(",")
        if origin.strip()
    ]


API_TITLE = os.getenv(
    "RETAILOPS_API_TITLE",
    "RetailOps AI API",
)

API_VERSION = os.getenv(
    "RETAILOPS_API_VERSION",
    "1.0.0",
)

API_DEBUG = _parse_bool(
    os.getenv(
        "RETAILOPS_API_DEBUG"
    ),
    False,
)

API_DOCS_ENABLED = _parse_bool(
    os.getenv(
        "RETAILOPS_API_DOCS_ENABLED"
    ),
    True,
)

CORS_ORIGINS = _parse_origins(
    os.getenv(
        "RETAILOPS_CORS_ORIGINS"
    )
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

RETAILOPS_API_KEY = os.getenv(
    "RETAILOPS_API_KEY"
)


def validate_production_config() -> None:
    """
    Validate configuration required for production.

    Development/test environments may omit secrets,
    but production must provide them.
    """

    environment = os.getenv(
        "RETAILOPS_ENV",
        "development",
    ).strip().lower()

    if environment not in {
        "development",
        "testing",
        "production",
    }:
        raise ValueError(
            "RETAILOPS_ENV must be "
            "development, testing, or production."
        )

    if environment != "production":
        return

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is required in production."
        )

    if GROQ_API_KEY.strip() == (
        "your-groq-api-key-here"
    ):
        raise ValueError(
            "GROQ_API_KEY still contains the "
            "placeholder value."
        )

    if not RETAILOPS_API_KEY:
        raise ValueError(
            "RETAILOPS_API_KEY is required in production."
        )

    if RETAILOPS_API_KEY.strip() == (
        "replace-with-a-secure-api-key"
    ):
        raise ValueError(
            "RETAILOPS_API_KEY still contains the "
            "placeholder value."
        )

    if API_DEBUG:
        raise ValueError(
            "RETAILOPS_API_DEBUG must be false "
            "in production."
        )

    if API_DOCS_ENABLED:
        raise ValueError(
            "RETAILOPS_API_DOCS_ENABLED must be false "
            "in production."
    )

    if not CORS_ORIGINS:
        raise ValueError(
            "RETAILOPS_CORS_ORIGINS must contain "
            "at least one origin in production."
        )