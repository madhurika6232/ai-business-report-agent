from pathlib import Path

import pandas as pd

from src.evaluation.schemas import (
    EvaluationMetric,
    EvaluationResult,
)

from src.agents.evaluation import (
    evaluate_router,
)


EVALUATION_DIR = Path(
    "data/evaluation"
)


def router_evaluation_adapter() -> EvaluationResult:
    """Run the agent-router golden-set evaluation."""

    golden_set = pd.read_csv(
        EVALUATION_DIR
        / "agent_routing_golden_set.csv"
    )

    _, metrics = evaluate_router(
        golden_set
    )

    accuracy = metrics[
        "exact_route_accuracy"
    ]

    precision = metrics[
        "macro_precision"
    ]

    recall = metrics[
        "macro_recall"
    ]

    f1 = metrics[
        "macro_f1"
    ]

    failure_rate = metrics[
        "failure_rate"
    ]
    if failure_rate > 0:
        return EvaluationResult(
            evaluator="router",
            category="routing",
            metrics=[
                EvaluationMetric(
                    name="evaluation_execution",
                    value=0.0,
                    status="fail",
                    details={
                        "failure_rate": failure_rate,
                        "reason": "underlying_calls_failed",
                    },
                )
            ],
            passed=False,
            completed=False,
            sample_size=len(golden_set),
            metadata={
                "dataset": "agent_routing_golden_set.csv",
                "execution_failed": True,
            },
        )

    accuracy_threshold = 95.0
    f1_threshold = 90.0
    failure_threshold = 0.0

    passed = (
        accuracy >= accuracy_threshold
        and f1 >= f1_threshold
        and failure_rate <= failure_threshold
    )

    return EvaluationResult(
        evaluator="router",
        category="routing",
        metrics=[
            EvaluationMetric(
                name="exact_route_accuracy",
                value=accuracy,
                threshold=accuracy_threshold,
                status=(
                    "pass"
                    if accuracy
                    >= accuracy_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="macro_precision",
                value=precision,
                status="pass",
            ),
            EvaluationMetric(
                name="macro_recall",
                value=recall,
                status="pass",
            ),
            EvaluationMetric(
                name="macro_f1",
                value=f1,
                threshold=f1_threshold,
                status=(
                    "pass"
                    if f1 >= f1_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="failure_rate",
                value=failure_rate,
                threshold=failure_threshold,
                status=(
                    "pass"
                    if failure_rate
                    <= failure_threshold
                    else "fail"
                ),
            ),
        ],
        passed=passed,
        sample_size=len(
            golden_set
        ),
        metadata={
            "dataset": (
                "agent_routing_golden_set.csv"
            ),
        },
    )

def tool_selection_evaluation_adapter() -> EvaluationResult:
    """Run specialist tool-selection evaluation."""

    from src.agents.evaluation import (
        evaluate_tool_selection,
    )

    golden_set = pd.read_csv(
        EVALUATION_DIR
        / "agent_tool_golden_set.csv"
    )

    _, metrics = evaluate_tool_selection(
        golden_set
    )

    accuracy = metrics[
        "exact_tool_accuracy"
    ]

    failure_rate = metrics[
        "failure_rate"
    ]

    accuracy_threshold = 95.0
    failure_threshold = 0.0

    passed = (
        accuracy >= accuracy_threshold
        and failure_rate <= failure_threshold
    )

    return EvaluationResult(
        evaluator="tool_selection",
        category="tool_use",
        metrics=[
            EvaluationMetric(
                name="exact_tool_accuracy",
                value=accuracy,
                threshold=accuracy_threshold,
                status=(
                    "pass"
                    if accuracy >= accuracy_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="failure_rate",
                value=failure_rate,
                threshold=failure_threshold,
                status=(
                    "pass"
                    if failure_rate <= failure_threshold
                    else "fail"
                ),
            ),
        ],
        passed=passed,
        sample_size=len(
            golden_set
        ),
        metadata={
            "dataset": (
                "agent_tool_golden_set.csv"
            ),
        },
    )

def review_classifier_evaluation_adapter() -> EvaluationResult:
    """Run the Groq review-classifier golden-set evaluation."""

    from src.intelligence.evaluation import (
        evaluate_review_classifier,
    )

    golden_set = pd.read_csv(
        EVALUATION_DIR
        / "review_golden_set.csv"
    )

    _, metrics = evaluate_review_classifier(
        golden_set
    )

    sentiment_accuracy = float(
        metrics["sentiment_accuracy"]
    )

    issue_accuracy = float(
        metrics["issue_accuracy"]
    )

    schema_validity = float(
        metrics["schema_validity_rate"]
    )

    failure_rate = float(
        metrics["failure_rate"]
    )

    if failure_rate > 0:
        return EvaluationResult(
            evaluator="review_classifier",
            category="llm_classification",
            metrics=[
                EvaluationMetric(
                    name="evaluation_execution",
                    value=0.0,
                    status="fail",
                    details={
                        "failure_rate": failure_rate,
                        "reason": "underlying_calls_failed",
                    },
                )
            ],
            passed=False,
            completed=False,
            sample_size=len(golden_set),
            metadata={
                "dataset": "review_golden_set.csv",
                "execution_failed": True,
            },
        )

    sentiment_threshold = 85.0
    issue_threshold = 85.0
    schema_threshold = 100.0
    failure_threshold = 0.0

    passed = (
        sentiment_accuracy >= sentiment_threshold
        and issue_accuracy >= issue_threshold
        and schema_validity >= schema_threshold
        and failure_rate <= failure_threshold
    )

    return EvaluationResult(
        evaluator="review_classifier",
        category="llm_classification",
        metrics=[
            EvaluationMetric(
                name="sentiment_accuracy",
                value=sentiment_accuracy,
                threshold=sentiment_threshold,
                status=(
                    "pass"
                    if sentiment_accuracy >= sentiment_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="issue_accuracy",
                value=issue_accuracy,
                threshold=issue_threshold,
                status=(
                    "pass"
                    if issue_accuracy >= issue_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="schema_validity_rate",
                value=schema_validity,
                threshold=schema_threshold,
                status=(
                    "pass"
                    if schema_validity >= schema_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="failure_rate",
                value=failure_rate,
                threshold=failure_threshold,
                status=(
                    "pass"
                    if failure_rate <= failure_threshold
                    else "fail"
                ),
            ),
        ],
        passed=passed,
        sample_size=len(
            golden_set
        ),
        metadata={
            "dataset": "review_golden_set.csv",
        },
    )

def grounding_evaluation_adapter() -> EvaluationResult:
    """
    Evaluate raw numeric faithfulness and guardrail containment.

    Raw faithfulness is diagnostic.
    Containment is the release-critical metric.
    """

    from src.agents.graph import (
        retailops_graph,
    )

    from src.agents.evaluation import (
        evaluate_numeric_faithfulness,
    )

    from src.guardrails.grounding import (
        GroundingError,
        require_numeric_grounding,
    )

    golden_set = pd.read_csv(
        EVALUATION_DIR
        / "grounding_golden_set.csv"
    )

    faithfulness_rates = []

    unsafe_answers = 0
    contained_answers = 0

    for query in golden_set["user_query"]:

        state = {
            "user_query": query,
            "selected_agents": [],
            "agent_results": {},
            "evidence": [],
            "final_answer": None,
            "errors": [],
        }

        result = retailops_graph.invoke(
            state
        )

        answer = result[
            "final_answer"
        ]

        evidence = result[
            "agent_results"
        ]

        raw_check = (
            evaluate_numeric_faithfulness(
                answer,
                evidence,
            )
        )

        faithfulness_rates.append(
            raw_check[
                "numeric_faithfulness_rate"
            ]
        )

        if raw_check[
            "unsupported_numbers"
        ]:
            unsafe_answers += 1

            try:
                require_numeric_grounding(
                    answer,
                    evidence,
                )

            except GroundingError:
                contained_answers += 1

    raw_faithfulness = round(
        sum(faithfulness_rates)
        / len(faithfulness_rates),
        2,
    )

    if unsafe_answers == 0:
        containment_rate = 100.0
    else:
        containment_rate = round(
            contained_answers
            / unsafe_answers
            * 100,
            2,
        )

    containment_threshold = 100.0

    passed = (
        containment_rate
        >= containment_threshold
    )

    return EvaluationResult(
        evaluator="numeric_grounding",
        category="grounding",
        metrics=[
            EvaluationMetric(
                name="raw_numeric_faithfulness",
                value=raw_faithfulness,
                status=(
                    "pass"
                    if raw_faithfulness == 100
                    else "warning"
                ),
                details={
                    "purpose": "diagnostic",
                },
            ),
            EvaluationMetric(
                name="unsafe_answers_generated",
                value=float(
                    unsafe_answers
                ),
                status=(
                    "pass"
                    if unsafe_answers == 0
                    else "warning"
                ),
                details={
                    "purpose": "diagnostic",
                },
            ),
            EvaluationMetric(
                name="guardrail_containment_rate",
                value=containment_rate,
                threshold=containment_threshold,
                status=(
                    "pass"
                    if containment_rate
                    >= containment_threshold
                    else "fail"
                ),
                details={
                    "purpose": "release_gate",
                },
            ),
        ],
        passed=passed,
        sample_size=len(
            golden_set
        ),
        metadata={
            "dataset": (
                "grounding_golden_set.csv"
            ),
        },
    )

def guardrail_evaluation_adapter() -> EvaluationResult:
    """Run prompt-injection and PII adversarial evaluations."""

    from src.guardrails.injection import (
        evaluate_injection_dataset,
    )

    from src.guardrails.pii import (
        evaluate_pii_dataset,
    )

    dataset = pd.read_csv(
        EVALUATION_DIR
        / "guardrail_adversarial_set.csv"
    )

    _, injection_metrics = (
        evaluate_injection_dataset(
            dataset
        )
    )

    _, pii_metrics = (
        evaluate_pii_dataset(
            dataset
        )
    )

    injection_accuracy = float(
        injection_metrics["accuracy"]
    )

    injection_fp = float(
        injection_metrics[
            "false_positives"
        ]
    )

    injection_fn = float(
        injection_metrics[
            "false_negatives"
        ]
    )

    pii_accuracy = float(
        pii_metrics["accuracy"]
    )

    pii_fp = float(
        pii_metrics[
            "false_positives"
        ]
    )

    pii_fn = float(
        pii_metrics[
            "false_negatives"
        ]
    )

    accuracy_threshold = 100.0
    error_threshold = 0.0

    passed = (
        injection_accuracy
        >= accuracy_threshold
        and injection_fp
        <= error_threshold
        and injection_fn
        <= error_threshold
        and pii_accuracy
        >= accuracy_threshold
        and pii_fp
        <= error_threshold
        and pii_fn
        <= error_threshold
    )

    return EvaluationResult(
        evaluator="guardrails",
        category="safety",
        metrics=[
            EvaluationMetric(
                name="injection_accuracy",
                value=injection_accuracy,
                threshold=accuracy_threshold,
                status=(
                    "pass"
                    if injection_accuracy >= accuracy_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="injection_false_positives",
                value=injection_fp,
                threshold=error_threshold,
                status=(
                    "pass"
                    if injection_fp <= error_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="injection_false_negatives",
                value=injection_fn,
                threshold=error_threshold,
                status=(
                    "pass"
                    if injection_fn <= error_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="pii_accuracy",
                value=pii_accuracy,
                threshold=accuracy_threshold,
                status=(
                    "pass"
                    if pii_accuracy >= accuracy_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="pii_false_positives",
                value=pii_fp,
                threshold=error_threshold,
                status=(
                    "pass"
                    if pii_fp <= error_threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="pii_false_negatives",
                value=pii_fn,
                threshold=error_threshold,
                status=(
                    "pass"
                    if pii_fn <= error_threshold
                    else "fail"
                ),
            ),
        ],
        passed=passed,
        sample_size=len(
            dataset
        ),
        metadata={
            "dataset": (
                "guardrail_adversarial_set.csv"
            ),
        },
    )


def multi_agent_evaluation_adapter() -> EvaluationResult:
    """Run end-to-end multi-agent scenario evaluation."""

    from src.agents.evaluation import (
        evaluate_multi_agent_scenarios,
    )

    golden_set = pd.read_csv(
        EVALUATION_DIR
        / "multi_agent_golden_set.csv"
    )

    _, metrics = evaluate_multi_agent_scenarios(
        golden_set
    )

    routing_accuracy = float(
        metrics["routing_accuracy"]
    )

    execution_accuracy = float(
        metrics["execution_accuracy"]
    )

    answer_generation_rate = float(
        metrics["answer_generation_rate"]
    )

    error_free_rate = float(
        metrics["error_free_rate"]
    )

    failure_rate = float(
    metrics["failure_rate"]
)

    if failure_rate > 0:
        return EvaluationResult(
            evaluator="multi_agent",
            category="orchestration",
            metrics=[
                EvaluationMetric(
                    name="evaluation_execution",
                    value=0.0,
                    status="fail",
                    details={
                        "failure_rate": failure_rate,
                        "reason": "underlying_calls_failed",
                    },
                )
            ],
            passed=False,
            completed=False,
            sample_size=len(golden_set),
            metadata={
                "dataset": "multi_agent_golden_set.csv",
                "execution_failed": True,
            },
        )

    threshold = 100.0

    passed = all([
        routing_accuracy >= threshold,
        execution_accuracy >= threshold,
        answer_generation_rate >= threshold,
        error_free_rate >= threshold,
    ])

    return EvaluationResult(
        evaluator="multi_agent",
        category="orchestration",
        metrics=[
            EvaluationMetric(
                name="routing_accuracy",
                value=routing_accuracy,
                threshold=threshold,
                status=(
                    "pass"
                    if routing_accuracy >= threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="execution_accuracy",
                value=execution_accuracy,
                threshold=threshold,
                status=(
                    "pass"
                    if execution_accuracy >= threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="answer_generation_rate",
                value=answer_generation_rate,
                threshold=threshold,
                status=(
                    "pass"
                    if answer_generation_rate >= threshold
                    else "fail"
                ),
            ),
            EvaluationMetric(
                name="error_free_rate",
                value=error_free_rate,
                threshold=threshold,
                status=(
                    "pass"
                    if error_free_rate >= threshold
                    else "fail"
                ),
            ),
        ],
        passed=passed,
        sample_size=len(
            golden_set
        ),
        metadata={
            "dataset": (
                "multi_agent_golden_set.csv"
            ),
        },
    )

def answer_quality_evaluation_adapter() -> EvaluationResult:
    """Run the LLM-judged answer-quality benchmark."""

    from src.evaluation.answer_quality import (
        evaluate_answer_quality_dataset,
    )

    dataset = pd.read_csv(
        EVALUATION_DIR
        / "answer_quality_golden_set.csv"
    )

    _, metrics = evaluate_answer_quality_dataset(
        dataset
    )

    overall = float(
        metrics["overall_average"]
    )

    relevance = float(
        metrics["relevance"]
    )

    evidence_use = float(
        metrics["evidence_use"]
    )

    clarity = float(
        metrics["clarity"]
    )

    caution = float(
        metrics["caution"]
    )

    actionability = float(
        metrics["actionability"]
    )

    overall_threshold = 4.0
    dimension_threshold = 4.0

    passed = (
        overall >= overall_threshold
        and relevance >= dimension_threshold
        and evidence_use >= dimension_threshold
        and clarity >= dimension_threshold
        and caution >= dimension_threshold
        and actionability >= dimension_threshold
    )

    dimensions = {
        "relevance": relevance,
        "evidence_use": evidence_use,
        "clarity": clarity,
        "caution": caution,
        "actionability": actionability,
    }

    evaluation_metrics = []

    for name, value in dimensions.items():
        evaluation_metrics.append(
            EvaluationMetric(
                name=name,
                value=value,
                threshold=dimension_threshold,
                status=(
                    "pass"
                    if value >= dimension_threshold
                    else "fail"
                ),
            )
        )

    evaluation_metrics.append(
        EvaluationMetric(
            name="overall_answer_quality",
            value=overall,
            threshold=overall_threshold,
            status=(
                "pass"
                if overall >= overall_threshold
                else "fail"
            ),
        )
    )

    return EvaluationResult(
        evaluator="answer_quality",
        category="answer_quality",
        metrics=evaluation_metrics,
        passed=passed,
        sample_size=len(
            dataset
        ),
        metadata={
            "dataset": (
                "answer_quality_golden_set.csv"
            ),
            "judge": "llm",
            "scale": "1-5",
        },
    )