import json
import logging
import sys
from datetime import datetime, timezone


LOGGER_NAME = "retailops.api"


class JsonFormatter(
    logging.Formatter
):
    """Format API logs as structured JSON."""

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in (
            "request_id",
            "method",
            "path",
            "status_code",
            "latency_ms",
            "error_type",
        ):
            value = getattr(
                record,
                field,
                None,
            )

            if value is not None:
                payload[field] = value

        return json.dumps(
            payload,
            ensure_ascii=False,
        )


def configure_logging() -> logging.Logger:
    """Configure the RetailOps API logger."""

    logger = logging.getLogger(
        LOGGER_NAME
    )

    logger.setLevel(
        logging.INFO
    )

    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(
            sys.stdout
        )

        handler.setFormatter(
            JsonFormatter()
        )

        logger.addHandler(
            handler
        )

    return logger


api_logger = configure_logging()