import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import (
    HTTPException,
    Request,
    status,
)


RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60


class InMemoryRateLimiter:
    """Simple fixed-window request limiter."""

    def __init__(
        self,
        max_requests: int = RATE_LIMIT_REQUESTS,
        window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests: dict[
            str,
            deque[float],
        ] = defaultdict(deque)

        self._lock = Lock()

    def check(
        self,
        key: str,
    ) -> None:
        """Reject requests exceeding the configured limit."""

        now = time.monotonic()

        cutoff = (
            now
            - self.window_seconds
        )

        with self._lock:

            timestamps = self._requests[
                key
            ]

            while (
                timestamps
                and timestamps[0] <= cutoff
            ):
                timestamps.popleft()

            if (
                len(timestamps)
                >= self.max_requests
            ):
                raise HTTPException(
                    status_code=(
                        status.HTTP_429_TOO_MANY_REQUESTS
                    ),
                    detail=(
                        "Too many requests. "
                        "Please try again later."
                    ),
                )

            timestamps.append(
                now
            )

    def clear(self) -> None:
        """Clear rate-limit state."""

        with self._lock:
            self._requests.clear()


rate_limiter = InMemoryRateLimiter()


def require_rate_limit(
    request: Request,
) -> None:
    """Apply rate limiting using the client address."""

    client_host = (
        request.client.host
        if request.client is not None
        else "unknown"
    )

    rate_limiter.check(
        client_host
    )