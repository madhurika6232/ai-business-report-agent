from fastapi import (
    APIRouter,
    status,
)

from src.api.schemas import (
    QueryRequest,
    QueryResponse,
)

from src.guardrails import (
    guarded_agent_query,
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
    tags=["query"],
    dependencies=[
        Depends(
            require_api_key
        ),
        Depends(
            require_rate_limit
        ),
    ],
)


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask RetailOps AI",
)
def query_retailops(
    request: QueryRequest,
) -> QueryResponse:
    """Run a business question through the guarded agent workflow."""

    result = guarded_agent_query(
        request.query
    )

    return QueryResponse(
        query=request.query,
        safe_query=result.get(
            "safe_query"
        ),
        answer=result.get(
            "final_answer",
            "",
        ),
        selected_agents=result.get(
            "selected_agents",
            [],
        ),
        blocked=result.get(
            "blocked",
            False,
        ),
        block_reason=result.get(
            "block_reason"
        ),
        pii_detected=result.get(
            "pii_detected",
            False,
        ),
        guardrail_validation=result.get(
            "guardrail_validation"
        ),
    )