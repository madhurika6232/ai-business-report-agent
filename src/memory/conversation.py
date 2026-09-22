from typing import Any, Literal

from pydantic import BaseModel, Field

from src.intelligence.groq_client import (
    DEFAULT_MODEL,
    get_groq_client,
)


MessageRole = Literal[
    "user",
    "assistant",
]


class ConversationTurn(BaseModel):
    """One turn in a RetailOps conversation."""

    role: MessageRole

    content: str = Field(
        min_length=1,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ConversationMemory(BaseModel):
    """Conversation history for one RetailOps session."""

    session_id: str = Field(
        min_length=1,
    )

    turns: list[ConversationTurn] = Field(
        default_factory=list,
    )

    last_query: str | None = None

    last_selected_agents: list[str] = Field(
        default_factory=list,
    )

    last_context: dict[str, Any] = Field(
        default_factory=dict,
    )

    def add_user_turn(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add a user message to memory."""

        self.turns.append(
            ConversationTurn(
                role="user",
                content=content,
                metadata=metadata or {},
            )
        )

        self.last_query = content

    def add_assistant_turn(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add an assistant response to memory."""

        self.turns.append(
            ConversationTurn(
                role="assistant",
                content=content,
                metadata=metadata or {},
            )
        )

    def recent_turns(
        self,
        limit: int = 6,
    ) -> list[ConversationTurn]:
        """Return the most recent conversation turns."""

        if limit <= 0:
            raise ValueError(
                "limit must be greater than 0."
            )

        return self.turns[-limit:]

def resolve_query_with_memory(
    user_query: str,
    memory: ConversationMemory,
) -> str:
    """Resolve a potentially contextual follow-up into a standalone query."""

    if not user_query or not user_query.strip():
        raise ValueError(
            "user_query cannot be empty."
        )

    # No history means there is nothing to resolve.
    if not memory.turns:
        return user_query

    recent = memory.recent_turns(
        limit=6
    )

    conversation = "\n".join(
        f"{turn.role}: {turn.content}"
        for turn in recent
    )

    client = get_groq_client()

    prompt = f"""
You resolve conversational follow-up questions for RetailOps AI.

Conversation history:
{conversation}

New user query:
{user_query}

Rewrite the NEW user query as a standalone business question
only when conversation context is necessary.

Rules:

1. Preserve explicit dates, metrics, categories, states, sellers,
   and other business dimensions from the conversation when needed.

2. Resolve references such as:
   - "that"
   - "those"
   - "previous month"
   - "same category"
   - "what about SP?"
   - "compare it"

3. Do not answer the question.

4. Do not invent information absent from the conversation.

5. If the new query is already standalone, return it unchanged.

6. Return only the resolved question.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Resolve conversational references without "
                    "answering the business question."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return (
        response.choices[0]
        .message.content
        .strip()
    )