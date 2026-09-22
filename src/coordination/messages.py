from typing import Any, Literal

from pydantic import BaseModel, Field


AgentName = Literal[
    "supervisor",
    "business",
    "operations",
    "customer",
    "risk",
]


MessageType = Literal[
    "request",
    "response",
    "error",
]


class AgentMessage(BaseModel):
    """Structured message exchanged between RetailOps agents."""

    sender: AgentName

    recipient: AgentName

    message_type: MessageType

    task: str = Field(
        min_length=1,
    )

    context: dict[str, Any] = Field(
        default_factory=dict,
    )

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )


class AgentResponse(BaseModel):
    """Structured response returned by a specialist agent."""

    agent: AgentName

    success: bool

    task: str

    evidence: dict[str, Any] = Field(
        default_factory=dict,
    )

    error: str | None = None