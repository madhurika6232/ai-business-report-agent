from datetime import datetime, timezone
from pathlib import Path

from src.evaluation.registry import (
    Evaluator,
    EvaluationRegistry,
)

from src.evaluation.schemas import (
    EvaluationMetric,
    EvaluationResult,
)

from src.evaluation.adapters import (
    router_evaluation_adapter,
    tool_selection_evaluation_adapter,
    review_classifier_evaluation_adapter,
    grounding_evaluation_adapter,
    guardrail_evaluation_adapter,
    multi_agent_evaluation_adapter,
    answer_quality_evaluation_adapter,
)

from src.evaluation.scorecard import (
    build_quality_scorecard,
)


# ============================================================
# EVALUATION REGISTRY
# ============================================================

def build_evaluation_registry() -> EvaluationRegistry:
    """Build the complete RetailOps evaluation registry."""

    registry = EvaluationRegistry()

    registry.register(
        Evaluator(
            name="router",
            category="routing",
            description=(
                "Evaluate agent-routing accuracy."
            ),
            handler=router_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="tool_selection",
            category="tool_use",
            description=(
                "Evaluate specialist tool selection."
            ),
            handler=tool_selection_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="review_classifier",
            category="llm_classification",
            description=(
                "Evaluate Groq review classification."
            ),
            handler=review_classifier_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="numeric_grounding",
            category="grounding",
            description=(
                "Evaluate raw numeric faithfulness "
                "and guardrail containment."
            ),
            handler=grounding_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="guardrails",
            category="safety",
            description=(
                "Evaluate prompt-injection and PII guardrails."
            ),
            handler=guardrail_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="multi_agent",
            category="orchestration",
            description=(
                "Evaluate multi-agent routing and execution."
            ),
            handler=multi_agent_evaluation_adapter,
        )
    )

    registry.register(
        Evaluator(
            name="answer_quality",
            category="answer_quality",
            description=(
                "Evaluate final-answer quality with "
                "the structured LLM judge."
            ),
            handler=answer_quality_evaluation_adapter,
        )
    )

    return registry


evaluation_registry = (
    build_evaluation_registry()
)


# ============================================================
# EVALUATION SUITE
# ============================================================

def run_evaluation_suite(
    evaluator_names: list[str] | None = None,
) -> dict:
    """
    Run selected evaluators and build the quality scorecard.

    Evaluation execution failures are captured as incomplete
    results rather than crashing the complete suite.
    """

    if evaluator_names is None:
        evaluator_names = [
            evaluator.name
            for evaluator
            in evaluation_registry.list_evaluators()
        ]

    if not evaluator_names:
        raise ValueError(
            "At least one evaluator must be selected."
        )

    results = []

    for name in evaluator_names:

        try:
            result = evaluation_registry.run(
                name
            )

        except Exception as error:

            evaluator = (
                evaluation_registry.get(
                    name
                )
            )

            result = EvaluationResult(
                evaluator=name,
                category=evaluator.category,
                metrics=[
                    EvaluationMetric(
                        name="evaluation_execution",
                        value=0.0,
                        threshold=100.0,
                        status="fail",
                        details={
                            "error_type": (
                                type(error).__name__
                            ),
                        },
                    )
                ],
                passed=False,
                completed=False,
                sample_size=0,
                metadata={
                    "execution_failed": True,
                },
            )

        results.append(
            result
        )

    return build_quality_scorecard(
        results
    )


# ============================================================
# MARKDOWN REPORT
# ============================================================

def save_evaluation_report(
    scorecard: dict,
    output_path: str | Path,
) -> Path:
    """Save a Markdown evaluation scorecard."""

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    suite = scorecard[
        "suite"
    ]

    lines = [
        "# RetailOps AI Evaluation Report",
        "",
        (
            "Generated: "
            + datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "",
        "## Summary",
        "",
        (
            f"- Overall score: "
            f"{suite.overall_score:.2f}/100"
        ),
        (
            f"- Release decision: "
            f"{scorecard['release_decision'].upper()}"
        ),
        (
            f"- Evaluators run: "
            f"{suite.total_evaluators}"
        ),
        "",
        "## Evaluator Scores",
        "",
        "| Evaluator | Score | Status |",
        "|---|---:|:---:|",
    ]

    # --------------------------------------------------------
    # Evaluator summary table
    # --------------------------------------------------------

    for result in suite.results:

        score = scorecard[
            "evaluator_scores"
        ][
            result.evaluator
        ]

        score_text = (
            f"{score:.2f}"
            if score is not None
            else "N/A"
        )

        status_text = (
            "Incomplete"
            if not result.completed
            else (
                "Pass"
                if result.passed
                else "Fail"
            )
        )

        lines.append(
            f"| {result.evaluator} "
            f"| {score_text} "
            f"| {status_text} |"
        )

    # --------------------------------------------------------
    # Detailed metrics
    # --------------------------------------------------------

    lines.extend([
        "",
        "## Detailed Metrics",
        "",
    ])

    for result in suite.results:

        lines.append(
            f"### {result.evaluator}"
        )

        lines.append("")

        if not result.completed:

            error_type = (
                result.metrics[0]
                .details
                .get(
                    "error_type",
                    "UnknownError",
                )
            )

            lines.append(
                "- Evaluation status: incomplete"
            )

            lines.append(
                f"- Execution error type: "
                f"{error_type}"
            )

            lines.append("")

            continue

        for metric in result.metrics:

            threshold = (
                str(metric.threshold)
                if metric.threshold
                is not None
                else "N/A"
            )

            lines.append(
                f"- {metric.name}: "
                f"{metric.value} "
                f"(threshold: {threshold}, "
                f"status: {metric.status})"
            )

        lines.append("")

    # --------------------------------------------------------
    # Release gate
    # --------------------------------------------------------

    critical_failures = scorecard.get(
        "critical_failures",
        [],
    )

    noncritical_failures = scorecard.get(
        "noncritical_failures",
        [],
    )

    incomplete_evaluators = scorecard.get(
        "incomplete_evaluators",
        [],
    )

    lines.extend([
        "## Release Gate",
        "",
        (
            "Critical failures: "
            + (
                ", ".join(
                    critical_failures
                )
                if critical_failures
                else "None"
            )
        ),
        "",
        (
            "Non-critical failures: "
            + (
                ", ".join(
                    noncritical_failures
                )
                if noncritical_failures
                else "None"
            )
        ),
        "",
        (
            "Incomplete evaluators: "
            + (
                ", ".join(
                    incomplete_evaluators
                )
                if incomplete_evaluators
                else "None"
            )
        ),
        "",
    ])

    # --------------------------------------------------------
    # Interpretation for incomplete suites
    # --------------------------------------------------------

    if incomplete_evaluators:

        lines.extend([
            "## Evaluation Status",
            "",
            (
                "This evaluation suite is incomplete. "
                "The overall score reflects only evaluators "
                "that completed successfully and must not be "
                "treated as a complete release benchmark."
            ),
            "",
        ])

    output_path.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )

    return output_path


# ============================================================
# BASELINE SNAPSHOT
# ============================================================

def save_scorecard_baseline(
    scorecard: dict,
    name: str,
    metadata: dict | None = None,
):
    """Save a complete quality scorecard as a regression baseline."""

    from src.evaluation.regression import (
        save_baseline,
    )

    if (
        scorecard[
            "release_decision"
        ]
        == "incomplete"
    ):
        raise ValueError(
            "Cannot save an incomplete evaluation "
            "suite as a release baseline."
        )

    evaluator_scores = {
        name: score
        for name, score
        in scorecard[
            "evaluator_scores"
        ].items()
        if score is not None
    }

    return save_baseline(
        name=name,
        evaluator_scores=evaluator_scores,
        overall_score=scorecard[
            "suite"
        ].overall_score,
        metadata={
            "release_decision": scorecard[
                "release_decision"
            ],
            **(
                metadata
                or {}
            ),
        },
    )