from typing import Any

from src.guardrails.policy import (
    guard_input,
    guard_output,
)
from src.guardrails.errors import (
    sanitize_error,
)
from src.guardrails.audit import (
    guardrail_audit_log,
)


def guarded_agent_query(
    user_query: str,
) -> dict[str, Any]:
    """
    Execute the RetailOps workflow through centralized
    guardrails and privacy-conscious audit logging.
    """

    try:
        # -------------------------
        # Input guardrails
        # -------------------------

        input_result = guard_input(
            user_query
        )

        safe_query = input_result.safe_query

        # Record PII redaction without storing raw PII.
        if input_result.pii.detected:
            guardrail_audit_log.record(
                event_type="pii",
                action="redacted",
                metadata={
                    "types": list(
                        input_result.pii.types
                    ),
                },
            )

        # -------------------------
        # Agent execution
        # -------------------------

        from src.agents.graph import (
            retailops_graph,
        )

        initial_state = {
            "user_query": safe_query,
            "selected_agents": [],
            "agent_results": {},
            "evidence": [],
            "final_answer": None,
            "errors": [],
        }

        result = retailops_graph.invoke(
            initial_state
        )

        if result["errors"]:
            raise RuntimeError(
                "; ".join(
                    result["errors"]
                )
            )

        # -------------------------
        # Output guardrails
        # -------------------------

        validation = guard_output(
            answer=result["final_answer"],
            evidence=result["agent_results"],
        )

        guardrail_audit_log.record(
            event_type="output_validation",
            action="passed",
            metadata={
                "numeric_faithfulness_rate": (
                    validation[
                        "numeric_grounding"
                    ][
                        "numeric_faithfulness_rate"
                    ]
                ),
            },
        )

        return {
            **result,
            "safe_query": safe_query,
            "pii_detected": (
                input_result.pii.detected
            ),
            "guardrail_validation": validation,
            "blocked": False,
        }

    except PermissionError as error:

        guardrail_audit_log.record(
            event_type="input_policy",
            action="blocked",
            metadata={
                "reason": type(error).__name__,
            },
        )

        return {
            "user_query": user_query,
            "final_answer": (
                "I can't process this request "
                "because it violates an input "
                "safety requirement."
            ),
            "errors": [],
            "blocked": True,
            "block_reason": type(error).__name__,
        }

    except ValueError as error:

        guardrail_audit_log.record(
            event_type="output_or_input_validation",
            action="blocked",
            metadata={
                "reason": type(error).__name__,
            },
        )

        return {
            "user_query": user_query,
            "final_answer": (
                "I can't process this request "
                "because it violates a safety "
                "or validation requirement."
            ),
            "errors": [],
            "blocked": True,
            "block_reason": type(error).__name__,
        }

    except Exception as error:

        guardrail_audit_log.record(
            event_type="internal_error",
            action="blocked",
            metadata={
                "error_type": type(error).__name__,
            },
        )

        return {
            "user_query": user_query,
            "final_answer": sanitize_error(
                error
            ),
            "errors": [],
            "blocked": True,
            "block_reason": "internal_error",
        }