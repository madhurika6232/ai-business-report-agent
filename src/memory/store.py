from src.memory.conversation import (
    ConversationMemory,
)


class MemoryStore:
    """In-memory store for RetailOps conversation sessions."""

    def __init__(self):
        self._sessions: dict[
            str,
            ConversationMemory,
        ] = {}

    def get_or_create(
        self,
        session_id: str,
    ) -> ConversationMemory:
        """Get an existing session or create a new one."""

        if not session_id or not session_id.strip():
            raise ValueError(
                "session_id cannot be empty."
            )

        if session_id not in self._sessions:
            self._sessions[
                session_id
            ] = ConversationMemory(
                session_id=session_id
            )

        return self._sessions[
            session_id
        ]

    def get(
        self,
        session_id: str,
    ) -> ConversationMemory | None:
        """Return a session if it exists."""

        return self._sessions.get(
            session_id
        )

    def delete(
        self,
        session_id: str,
    ) -> bool:
        """Delete a conversation session."""

        if session_id not in self._sessions:
            return False

        del self._sessions[
            session_id
        ]

        return True

    def clear(self) -> None:
        """Delete all conversation sessions."""

        self._sessions.clear()

    def __len__(self) -> int:
        return len(self._sessions)


memory_store = MemoryStore()

from typing import Any

from src.memory.conversation import (
    resolve_query_with_memory,
)


def answer_with_memory(
    user_query: str,
    session_id: str,
    store: MemoryStore | None = None,
) -> dict[str, Any]:
    """Run the RetailOps agent workflow with conversation memory."""

    if not user_query or not user_query.strip():
        raise ValueError(
            "user_query cannot be empty."
        )

    active_store = (
        store
        if store is not None
        else memory_store
    )

    memory = active_store.get_or_create(
        session_id
    )

    # Resolve references BEFORE adding the new
    # user turn to conversation history.
    resolved_query = resolve_query_with_memory(
        user_query,
        memory,
    )

    # Import here to avoid unnecessary circular imports.
    from src.agents.graph import retailops_graph

    initial_state = {
        "user_query": resolved_query,
        "selected_agents": [],
        "agent_results": {},
        "evidence": [],
        "final_answer": None,
        "errors": [],
    }

    result = retailops_graph.invoke(
        initial_state
    )

    # Store the original user wording.
    memory.add_user_turn(
        user_query,
        metadata={
            "resolved_query": resolved_query,
        },
    )

    memory.add_assistant_turn(
        result["final_answer"],
        metadata={
            "selected_agents": result[
                "selected_agents"
            ],
        },
    )

    memory.last_selected_agents = list(
        result["selected_agents"]
    )

    memory.last_context = {
        "resolved_query": resolved_query,
    }

    return {
        **result,
        "original_query": user_query,
        "resolved_query": resolved_query,
        "session_id": session_id,
    }