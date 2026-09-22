from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from src.api.schemas import (
    ConversationRequest,
    ConversationResponse,
)

from src.memory.store import (
    answer_with_memory,
    memory_store,
)

from fastapi import Depends

from src.api.security import (
    require_api_key,
)

from src.api.rate_limit import (
    require_rate_limit,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["sessions"],
    dependencies=[
        Depends(
            require_api_key
        ),
    ],
)

# ============================================================
# CONVERSATION
# ============================================================

@router.post(
    "/conversation",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask RetailOps AI with conversation memory",
    dependencies=[
        Depends(
            require_rate_limit
        ),
    ],
)
def conversation_query(
    request: ConversationRequest,
) -> ConversationResponse:
    """Run a memory-aware RetailOps conversation turn."""

    result = answer_with_memory(
        user_query=request.query,
        session_id=request.session_id,
        store=memory_store,
    )

    return ConversationResponse(
        session_id=result[
            "session_id"
        ],
        original_query=result[
            "original_query"
        ],
        resolved_query=result[
            "resolved_query"
        ],
        answer=result[
            "final_answer"
        ],
        selected_agents=result.get(
            "selected_agents",
            [],
        ),
    )


# ============================================================
# SESSION SUMMARY
# ============================================================

@router.get(
    "/sessions/{session_id}",
    summary="Get conversation session",
)
def get_session(
    session_id: str,
) -> dict:
    """Return a summary of an existing conversation session."""

    memory = memory_store.get(
        session_id
    )

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    return {
        "session_id": memory.session_id,
        "turn_count": len(
            memory.turns
        ),
        "last_query": memory.last_query,
        "last_selected_agents": (
            memory.last_selected_agents
        ),
    }


# ============================================================
# DELETE SESSION
# ============================================================

@router.delete(
    "/sessions/{session_id}",
    summary="Delete conversation session",
)
def delete_session(
    session_id: str,
) -> dict:
    """Delete an existing conversation session."""

    deleted = memory_store.delete(
        session_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    return {
        "session_id": session_id,
        "deleted": True,
    }