from fastapi import (
    FastAPI,
    Request,
    status,
)

from fastapi.responses import JSONResponse

from src.guardrails.errors import (
    sanitize_error,
)


def register_error_handlers(
    app: FastAPI,
) -> None:
    """Register safe global API exception handlers."""

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Return a sanitized response for unexpected errors."""

        safe_message = sanitize_error(
            exc
        )

        return JSONResponse(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            content={
                "error": "internal_error",
                "detail": safe_message,
            },
        )