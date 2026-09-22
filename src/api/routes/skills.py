from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from src.skills import (
    retailops_skills,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["skills"],
)


@router.get(
    "/skills",
    summary="List RetailOps skills",
)
def list_skills(
    domain: str | None = None,
) -> dict:
    """Return the public RetailOps skill catalog."""

    valid_domains = {
        "business",
        "operations",
        "customer",
        "risk",
    }

    if (
        domain is not None
        and domain not in valid_domains
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown skill domain.",
        )

    skills = retailops_skills.list_skills(
        domain=domain
    )

    return {
        "count": len(skills),
        "domain": domain,
        "skills": [
            {
                "name": skill.name,
                "domain": skill.domain,
                "description": skill.description,
            }
            for skill in skills
        ],
    }