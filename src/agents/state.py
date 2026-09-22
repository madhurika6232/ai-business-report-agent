from typing import Any, TypedDict


class AgentState(TypedDict):
    """Shared state passed through the RetailOps agent graph."""

    # Original user request
    user_query: str

    # Routing
    selected_agents: list[str]

    # Results returned by specialist agents/tools
    agent_results: dict[str, Any]

    # Evidence collected for final synthesis
    evidence: list[dict[str, Any]]

    # Final user-facing response
    final_answer: str | None

    # Error tracking
    errors: list[str]