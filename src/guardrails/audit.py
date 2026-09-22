from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class GuardrailEvent:
    """Privacy-conscious record of a guardrail event."""

    event_type: str
    action: str
    timestamp: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


class GuardrailAuditLog:
    """In-memory audit log for guardrail events."""

    def __init__(self):
        self._events: list[
            GuardrailEvent
        ] = []

    def record(
        self,
        event_type: str,
        action: str,
        metadata: dict[str, Any] | None = None,
    ) -> GuardrailEvent:
        """Record a guardrail event."""

        event = GuardrailEvent(
            event_type=event_type,
            action=action,
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),
            metadata=metadata or {},
        )

        self._events.append(
            event
        )

        return event

    def list_events(
        self,
        event_type: str | None = None,
    ) -> list[GuardrailEvent]:
        """Return recorded events."""

        if event_type is None:
            return list(
                self._events
            )

        return [
            event
            for event in self._events
            if event.event_type
            == event_type
        ]

    def clear(self) -> None:
        """Clear the audit log."""

        self._events.clear()

    def __len__(self) -> int:
        return len(self._events)


guardrail_audit_log = (
    GuardrailAuditLog()
)