from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from src.agents.state import AgentState
from src.agents.router import route_query
from src.agents.business_agent import run_business_agent
from src.agents.operations_agent import run_operations_agent
from src.agents.customer_agent import run_customer_agent
from src.agents.risk_agent import run_risk_agent
from src.agents.supervisor import synthesize_answer


# ============================================================
# AGENT REGISTRY
# ============================================================

AGENT_RUNNERS = {
    "business": run_business_agent,
    "operations": run_operations_agent,
    "customer": run_customer_agent,
    "risk": run_risk_agent,
}


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(
    state: AgentState,
) -> dict:
    """Route the user query to specialist agents."""

    decision = route_query(
        state["user_query"]
    )

    return {
        "selected_agents": decision.selected_agents,
    }


# ============================================================
# SPECIALIST NODE
# ============================================================

def specialist_node(
    state: AgentState,
) -> dict:
    """Execute all specialist agents selected by the router."""

    agent_results = {}
    evidence = []
    errors = []

    for agent_name in state["selected_agents"]:

        runner = AGENT_RUNNERS.get(
            agent_name
        )

        if runner is None:
            errors.append(
                f"Unknown agent: {agent_name}"
            )
            continue

        try:
            result = runner(
                state["user_query"]
            )

            agent_results[
                agent_name
            ] = result

            evidence.append({
                "agent": agent_name,
                "results": result["results"],
            })

        except Exception as error:
            errors.append(
                f"{agent_name}: {str(error)}"
            )

    return {
        "agent_results": agent_results,
        "evidence": evidence,
        "errors": errors,
    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_after_specialists(
    state: AgentState,
) -> str:
    """Choose whether to synthesize or return an error."""

    if state["errors"]:
        return "error"

    return "synthesis"


# ============================================================
# ERROR NODE
# ============================================================

def error_node(
    state: AgentState,
) -> dict:
    """Return a safe response when specialist execution fails."""

    return {
        "final_answer": (
            "I could not complete the requested analysis. "
            + "; ".join(state["errors"])
        )
    }


# ============================================================
# SYNTHESIS NODE
# ============================================================

def synthesis_node(
    state: AgentState,
) -> dict:
    """Generate the final grounded response."""

    supervisor_result = {
        "user_query": state["user_query"],
        "selected_agents": state["selected_agents"],
        "agent_results": state["agent_results"],
    }

    answer = synthesize_answer(
        supervisor_result
    )

    return {
        "final_answer": answer,
    }


# ============================================================
# BUILD LANGGRAPH
# ============================================================

def build_retailops_graph():
    """Build and compile the RetailOps LangGraph workflow."""

    builder = StateGraph(
        AgentState
    )

    # -------------------------
    # Nodes
    # -------------------------

    builder.add_node(
        "router",
        router_node,
    )

    builder.add_node(
        "specialists",
        specialist_node,
    )

    builder.add_node(
        "synthesis",
        synthesis_node,
    )

    builder.add_node(
        "error",
        error_node,
    )

    # -------------------------
    # Graph flow
    # -------------------------

    builder.add_edge(
        START,
        "router",
    )

    builder.add_edge(
        "router",
        "specialists",
    )

    builder.add_conditional_edges(
        "specialists",
        route_after_specialists,
        {
            "synthesis": "synthesis",
            "error": "error",
        },
    )

    builder.add_edge(
        "synthesis",
        END,
    )

    builder.add_edge(
        "error",
        END,
    )

    return builder.compile()


# ============================================================
# COMPILED APPLICATION GRAPH
# ============================================================

retailops_graph = build_retailops_graph()