from pathlib import Path

import yaml


PROJECT_ROOT = Path(
    __file__,
).resolve().parents[2]

DOCKERFILE_PATH = (
    PROJECT_ROOT
    / "Dockerfile"
)

COMPOSE_PATH = (
    PROJECT_ROOT
    / "docker-compose.yml"
)

FRONTEND_DOCKERFILE_PATH = (
    PROJECT_ROOT
    / "frontend"
    / "Dockerfile"
)


def load_compose():
    with COMPOSE_PATH.open(
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(
            file
        )


def test_backend_dockerfile_exists():
    assert (
        DOCKERFILE_PATH.exists()
    )


def test_frontend_dockerfile_exists():
    assert (
        FRONTEND_DOCKERFILE_PATH.exists()
    )


def test_compose_file_exists():
    assert (
        COMPOSE_PATH.exists()
    )


def test_compose_services():
    compose = load_compose()

    services = compose[
        "services"
    ]

    assert "backend" in services
    assert "frontend" in services


def test_backend_service_configuration():
    compose = load_compose()

    backend = compose[
        "services"
    ][
        "backend"
    ]

    assert (
        backend["image"]
        == "retailops-ai:phase13"
    )

    assert (
        backend["container_name"]
        == "retailops-backend"
    )

    assert (
        backend["build"]["context"]
        == "."
    )

    assert (
        backend["build"]["dockerfile"]
        == "Dockerfile"
    )

    assert (
        "8000"
        in backend["expose"]
    )


def test_frontend_service_configuration():
    compose = load_compose()

    frontend = compose[
        "services"
    ][
        "frontend"
    ]

    assert (
        frontend["image"]
        == "retailops-frontend:phase13"
    )

    assert (
        frontend["container_name"]
        == "retailops-frontend"
    )

    assert (
        frontend["build"]["context"]
        == "./frontend"
    )

    assert (
        frontend["build"]["dockerfile"]
        == "Dockerfile"
    )

    assert (
        "8080:80"
        in frontend["ports"]
    )


def test_backend_has_healthcheck():
    compose = load_compose()

    backend = compose[
        "services"
    ][
        "backend"
    ]

    assert (
        "healthcheck"
        in backend
    )

    healthcheck = backend[
        "healthcheck"
    ]

    assert "test" in healthcheck
    assert "interval" in healthcheck
    assert "timeout" in healthcheck
    assert "retries" in healthcheck


def test_frontend_has_healthcheck():
    compose = load_compose()

    frontend = compose[
        "services"
    ][
        "frontend"
    ]

    assert (
        "healthcheck"
        in frontend
    )

    healthcheck = frontend[
        "healthcheck"
    ]

    assert "test" in healthcheck
    assert "interval" in healthcheck
    assert "timeout" in healthcheck
    assert "retries" in healthcheck


def test_frontend_depends_on_backend_health():
    compose = load_compose()

    frontend = compose[
        "services"
    ][
        "frontend"
    ]

    dependency = frontend[
        "depends_on"
    ][
        "backend"
    ]

    assert (
        dependency["condition"]
        == "service_healthy"
    )


def test_frontend_uses_runtime_environment():
    compose = load_compose()

    frontend = compose[
        "services"
    ][
        "frontend"
    ]

    assert (
        ".env"
        in frontend["env_file"]
    )


def test_backend_not_exposed_to_host():
    compose = load_compose()

    backend = compose[
        "services"
    ][
        "backend"
    ]

    assert "ports" not in backend

    assert (
        "8000"
        in backend["expose"]
    )