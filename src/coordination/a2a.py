from src.coordination.messages import (
    AgentMessage,
    AgentResponse,
    AgentName,
)

from src.agents.business_agent import (
    run_business_agent,
)
from src.agents.operations_agent import (
    run_operations_agent,
)
from src.agents.customer_agent import (
    run_customer_agent,
)
from src.agents.risk_agent import (
    run_risk_agent,
)


AGENT_HANDLERS = {
    "business": run_business_agent,
    "operations": run_operations_agent,
    "customer": run_customer_agent,
    "risk": run_risk_agent,
}


def dispatch_message(
    message: AgentMessage,
) -> AgentResponse:
    """Dispatch a structured message to a specialist agent."""

    if message.message_type != "request":
        return AgentResponse(
            agent=message.recipient,
            success=False,
            task=message.task,
            error=(
                "Only request messages can be dispatched."
            ),
        )

    if message.recipient == "supervisor":
        return AgentResponse(
            agent="supervisor",
            success=False,
            task=message.task,
            error=(
                "Supervisor is not a specialist dispatch target."
            ),
        )

    handler = AGENT_HANDLERS.get(
        message.recipient
    )

    if handler is None:
        return AgentResponse(
            agent=message.recipient,
            success=False,
            task=message.task,
            error=(
                f"No handler registered for "
                f"{message.recipient}."
            ),
        )

    user_query = message.context.get(
        "user_query",
        message.task,
    )

    try:
        result = handler(
            user_query
        )

        return AgentResponse(
            agent=message.recipient,
            success=True,
            task=message.task,
            evidence=result["results"],
        )

    except Exception as error:
        return AgentResponse(
            agent=message.recipient,
            success=False,
            task=message.task,
            error=str(error),
        )


def dispatch_to_agents(
    user_query: str,
    agent_names: list[AgentName],
) -> dict[str, AgentResponse]:
    """Dispatch a user query to multiple specialist agents."""

    if not user_query or not user_query.strip():
        raise ValueError(
            "user_query cannot be empty."
        )

    if not agent_names:
        raise ValueError(
            "agent_names cannot be empty."
        )

    responses = {}

    for agent_name in agent_names:

        message = AgentMessage(
            sender="supervisor",
            recipient=agent_name,
            message_type="request",
            task=user_query,
            context={
                "user_query": user_query,
            },
        )

        response = dispatch_message(
            message
        )

        responses[agent_name] = response

    return responses