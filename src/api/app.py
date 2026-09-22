import time
import uuid

from fastapi import (
    FastAPI,
    Request,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from src.api.lifecycle import (
    application_lifespan,
)

from src.api.config import (
    API_DEBUG,
    API_TITLE,
    API_VERSION,
    CORS_ORIGINS,
)

from src.api.dependencies import (
    REQUEST_ID_HEADER,
)

from src.api.errors import (
    register_error_handlers,
)

from src.api.logging_config import (
    api_logger,
)

from src.api.routes.evaluation import (
    router as evaluation_router,
)

from src.api.routes.health import (
    router as health_router,
)

from src.api.routes.query import (
    router as query_router,
)

from src.api.routes.sessions import (
    router as sessions_router,
)

from src.api.routes.skills import (
    router as skills_router,
)

from src.api.config import (
    API_DEBUG,
    API_DOCS_ENABLED,
    API_TITLE,
    API_VERSION,
    CORS_ORIGINS,
)

def create_app() -> FastAPI:
    """Create the RetailOps AI API application."""

    app = FastAPI(
        title=API_TITLE,
        description=(
            "API for retail analytics, "
            "multi-agent intelligence, "
            "and guarded business insights."
        ),
        version=API_VERSION,
        debug=API_DEBUG,
        lifespan=application_lifespan,
        docs_url=(
            "/docs"
            if API_DOCS_ENABLED
            else None
        ),
        redoc_url=(
            "/redoc"
            if API_DOCS_ENABLED
            else None
        ),
        openapi_url=(
            "/openapi.json"
            if API_DOCS_ENABLED
            else None
        ),
    )

    # --------------------------------------------------------
    # CORS
    # --------------------------------------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "DELETE",
        ],
    allow_headers=[
        "Content-Type",
        "X-Request-ID",
        "X-API-Key",
    ],
    )

    # --------------------------------------------------------
    # Request ID + structured logging middleware
    # --------------------------------------------------------

    @app.middleware("http")
    async def request_id_middleware(
        request: Request,
        call_next,
    ):
        """
        Attach a correlation ID and safely log
        request completion metadata.
        """

        request_id = request.headers.get(
            REQUEST_ID_HEADER
        )

        if not request_id:
            request_id = str(
                uuid.uuid4()
            )

        request.state.request_id = (
            request_id
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(
                request
            )

        except Exception as error:
            latency_ms = round(
                (
                    time.perf_counter()
                    - start_time
                )
                * 1000,
                2,
            )

            api_logger.error(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "latency_ms": latency_ms,
                    "error_type": (
                        type(error).__name__
                    ),
                },
            )

            raise

        latency_ms = round(
            (
                time.perf_counter()
                - start_time
            )
            * 1000,
            2,
        )

        response.headers[
            REQUEST_ID_HEADER
        ] = request_id

        api_logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": (
                    response.status_code
                ),
                "latency_ms": latency_ms,
            },
        )

        return response

    # --------------------------------------------------------
    # Global error handling
    # --------------------------------------------------------

    register_error_handlers(
        app
    )

    # --------------------------------------------------------
    # API routes
    # --------------------------------------------------------

    app.include_router(
        health_router,
    )

    app.include_router(
        query_router,
    )

    app.include_router(
        sessions_router,
    )

    app.include_router(
        skills_router,
    )

    app.include_router(
        evaluation_router,
    )

    return app


app = create_app()