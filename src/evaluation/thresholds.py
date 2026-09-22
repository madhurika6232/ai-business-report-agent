RELEASE_THRESHOLDS = {
    "router": {
        "exact_route_accuracy": 95.0,
        "macro_f1": 90.0,
        "failure_rate": 0.0,
    },

    "tool_selection": {
        "exact_tool_accuracy": 95.0,
        "failure_rate": 0.0,
    },

    "review_classifier": {
        "sentiment_accuracy": 85.0,
        "issue_accuracy": 85.0,
        "schema_validity_rate": 100.0,
        "failure_rate": 0.0,
    },

    "numeric_grounding": {
        # Raw faithfulness is diagnostic.
        # The release-critical requirement is containment.
        "guardrail_containment_rate": 100.0,
    },

    "guardrails": {
        "injection_accuracy": 100.0,
        "injection_false_positives": 0.0,
        "injection_false_negatives": 0.0,
        "pii_accuracy": 100.0,
        "pii_false_positives": 0.0,
        "pii_false_negatives": 0.0,
    },

    "multi_agent": {
        "routing_accuracy": 100.0,
        "execution_accuracy": 100.0,
        "answer_generation_rate": 100.0,
        "error_free_rate": 100.0,
    },

    "answer_quality": {
        "relevance": 4.0,
        "evidence_use": 4.0,
        "clarity": 4.0,
        "caution": 4.0,
        "actionability": 4.0,
        "overall_answer_quality": 4.0,
    },
}


CRITICAL_EVALUATORS = {
    "router",
    "tool_selection",
    "numeric_grounding",
    "guardrails",
    "multi_agent",
}


def get_threshold(
    evaluator: str,
    metric: str,
) -> float:
    """Return the configured release threshold."""

    if evaluator not in RELEASE_THRESHOLDS:
        raise KeyError(
            f"Unknown evaluator: {evaluator}"
        )

    metrics = RELEASE_THRESHOLDS[
        evaluator
    ]

    if metric not in metrics:
        raise KeyError(
            f"Unknown metric for {evaluator}: {metric}"
        )

    return metrics[
        metric
    ]


def is_critical_evaluator(
    evaluator: str,
) -> bool:
    """Return whether evaluator failure blocks release."""

    return evaluator in CRITICAL_EVALUATORS