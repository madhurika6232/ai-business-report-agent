from dataclasses import dataclass
from typing import Any

from src.guardrails.input_validation import (
    normalize_user_query,
)
from src.guardrails.injection import (
    InjectionCheck,
    detect_prompt_injection,
)
from src.guardrails.pii import (
    PIICheck,
    detect_pii,
    redact_pii,
)
from src.guardrails.authorization import (
    require_skill_authorization,
)
from src.guardrails.grounding import (
    require_numeric_grounding,
)
from src.guardrails.output_validation import (
    require_valid_output,
)


@dataclass(frozen=True)
class InputGuardrailResult:
    """Validated input ready for agent processing."""

    original_query: str
    safe_query: str
    injection: InjectionCheck
    pii: PIICheck


def guard_input(
    user_query: str,
) -> InputGuardrailResult:
    """Apply input guardrails before agent execution."""

    normalized = normalize_user_query(
        user_query
    )

    injection = detect_prompt_injection(
        normalized
    )

    # Direct prompt-injection attempts are blocked.
    if injection.detected:
        raise PermissionError(
            "The request contains instructions "
            "that are not permitted."
        )

    pii = detect_pii(
        normalized
    )

    safe_query = (
        redact_pii(normalized)
        if pii.detected
        else normalized
    )

    return InputGuardrailResult(
        original_query=normalized,
        safe_query=safe_query,
        injection=injection,
        pii=pii,
    )


def guard_skill_execution(
    agent: str,
    skill: str,
) -> None:
    """Authorize an agent before skill execution."""

    require_skill_authorization(
        agent,
        skill,
    )


def guard_output(
    answer: str,
    evidence: Any,
) -> dict:
    """Validate an AI answer before user delivery."""

    output_validation = (
        require_valid_output(
            answer
        )
    )

    grounding_validation = (
        require_numeric_grounding(
            answer,
            evidence,
        )
    )

    return {
        "output_valid": (
            output_validation.valid
        ),
        "numeric_grounding": (
            grounding_validation
        ),
    }