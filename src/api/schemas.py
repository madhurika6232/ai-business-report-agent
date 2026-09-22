from typing import Any

from pydantic import (
    BaseModel,
    Field,
)


class QueryRequest(BaseModel):
    """Request to the RetailOps AI agent."""

    query: str = Field(
        min_length=1,
        max_length=2000,
        description="Business question for RetailOps AI.",
    )


class QueryResponse(BaseModel):
    """Response from the guarded RetailOps AI workflow."""

    query: str

    safe_query: str | None = None

    answer: str

    selected_agents: list[str] = Field(
        default_factory=list,
    )

    blocked: bool = False

    block_reason: str | None = None

    pii_detected: bool = False

    guardrail_validation: dict[
        str,
        Any,
    ] | None = None


class ConversationRequest(BaseModel):
    """Request for a memory-aware conversation."""

    query: str = Field(
        min_length=1,
        max_length=2000,
    )

    session_id: str = Field(
        min_length=1,
        max_length=100,
    )


class ConversationResponse(BaseModel):
    """Response from a memory-aware conversation."""

    session_id: str

    original_query: str

    resolved_query: str

    answer: str

    selected_agents: list[str] = Field(
        default_factory=list,
    )


class SessionSummary(BaseModel):
    """Summary of a conversation session."""

    session_id: str

    turn_count: int = Field(
        ge=0,
    )

    last_query: str | None = None


class SkillSummary(BaseModel):
    """Public description of a RetailOps skill."""

    name: str

    domain: str

    description: str


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: str

    detail: str | None = None

    request_id: str | None = None