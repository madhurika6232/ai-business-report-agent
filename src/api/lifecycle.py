from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.config import (
    validate_production_config,
)

from src.api.logging_config import (
    api_logger,
)

from src.memory.store import (
    memory_store,
)


@asynccontextmanager
async def application_lifespan(
    app: FastAPI,
):
    """Manage RetailOps API startup and shutdown."""

    validate_production_config()

    api_logger.info(
        "application_started"
    )

    try:
        yield

    finally:
        memory_store.clear()

        api_logger.info(
            "application_stopped"
        )