import uuid

from fastapi import Request


REQUEST_ID_HEADER = "X-Request-ID"


def get_request_id(
    request: Request,
) -> str:
    """Return the request correlation ID."""

    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    if request_id is None:
        request_id = str(
            uuid.uuid4()
        )

        request.state.request_id = (
            request_id
        )

    return request_id