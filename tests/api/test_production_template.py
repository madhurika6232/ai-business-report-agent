from pathlib import Path


PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)

TEMPLATE = (
    PROJECT_ROOT
    / ".env.production.example"
)


def test_production_template_exists():
    assert TEMPLATE.exists()


def test_production_template_has_required_settings():
    content = TEMPLATE.read_text(
        encoding="utf-8"
    )

    required = [
        "RETAILOPS_ENV=production",
        "GROQ_API_KEY=",
        "RETAILOPS_API_KEY=",
        "RETAILOPS_API_DEBUG=false",
        "RETAILOPS_API_DOCS_ENABLED=false",
        "RETAILOPS_CORS_ORIGINS=",
    ]

    for setting in required:
        assert setting in content


def test_production_template_does_not_enable_debug():
    content = TEMPLATE.read_text(
        encoding="utf-8"
    )

    assert (
        "RETAILOPS_API_DEBUG=true"
        not in content
    )


def test_production_template_does_not_enable_docs():
    content = TEMPLATE.read_text(
        encoding="utf-8"
    )

    assert (
        "RETAILOPS_API_DOCS_ENABLED=true"
        not in content
    )