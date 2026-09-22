import pandas as pd
import json
import re
import time

from sklearn.metrics import (
    precision_recall_fscore_support,
)

from src.agents.router import route_query


VALID_AGENTS = [
    "business",
    "operations",
    "customer",
    "risk",
]


# ============================================================
# GROQ EVALUATION PACING
# ============================================================

GROQ_EVALUATION_DELAY_SECONDS = 2.0


def _pace_groq_evaluation() -> None:
    """Pause between Groq-backed evaluation cases."""

    time.sleep(
        GROQ_EVALUATION_DELAY_SECONDS
    )


# ============================================================
# ROUTER EVALUATION
# ============================================================

def evaluate_router(
    golden_set: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Evaluate Groq routing against expected agent selections."""

    results = []

    for _, row in golden_set.iterrows():

        expected = set(
            str(row["expected_agents"]).split("|")
        )

        try:
            decision = route_query(
                row["user_query"]
            )

            predicted = set(
                decision.selected_agents
            )

            failed = False

        except Exception as error:
            predicted = set()
            failed = True

            print(
                "ROUTER EVALUATION ERROR:",
                type(error).__name__,
                str(error),
            )

        results.append({
            "user_query": row["user_query"],
            "expected_agents": "|".join(
                sorted(expected)
            ),
            "predicted_agents": "|".join(
                sorted(predicted)
            ),
            "exact_match": expected == predicted,
            "failed": failed,
        })

        # Router uses Groq.
        _pace_groq_evaluation()

    result_df = pd.DataFrame(
        results
    )

    expected_matrix = []
    predicted_matrix = []

    for _, row in result_df.iterrows():

        expected = set(
            row["expected_agents"].split("|")
        )

        predicted = (
            set(row["predicted_agents"].split("|"))
            if row["predicted_agents"]
            else set()
        )

        expected_matrix.append([
            int(agent in expected)
            for agent in VALID_AGENTS
        ])

        predicted_matrix.append([
            int(agent in predicted)
            for agent in VALID_AGENTS
        ])

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            expected_matrix,
            predicted_matrix,
            average="macro",
            zero_division=0,
        )
    )

    metrics = {
        "total_queries": len(result_df),

        "exact_route_accuracy": round(
            float(
                result_df[
                    "exact_match"
                ].mean()
            ) * 100,
            2,
        ),

        "macro_precision": round(
            float(precision) * 100,
            2,
        ),

        "macro_recall": round(
            float(recall) * 100,
            2,
        ),

        "macro_f1": round(
            float(f1) * 100,
            2,
        ),

        "failure_rate": round(
            float(
                result_df[
                    "failed"
                ].mean()
            ) * 100,
            2,
        ),
    }

    return result_df, metrics


# ============================================================
# TOOL SELECTION EVALUATION
# ============================================================

def evaluate_tool_selection(
    golden_set: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Evaluate specialist-agent tool selection."""

    from src.agents.business_agent import (
        run_business_agent,
    )
    from src.agents.operations_agent import (
        run_operations_agent,
    )
    from src.agents.customer_agent import (
        run_customer_agent,
    )
    from src.agents.risk_agent import (
        run_risk_agent,
    )

    runners = {
        "business": run_business_agent,
        "operations": run_operations_agent,
        "customer": run_customer_agent,
        "risk": run_risk_agent,
    }

    results = []

    for _, row in golden_set.iterrows():

        agent_name = row["agent"]

        expected = set(
            str(
                row["expected_tools"]
            ).split("|")
        )

        runner = runners.get(
            agent_name
        )

        if runner is None:
            predicted = set()
            failed = True

        else:
            try:
                output = runner(
                    row["user_query"]
                )

                predicted = set(
                    output[
                        "results"
                    ].keys()
                )

                failed = False

            except Exception:
                predicted = set()
                failed = True

        results.append({
            "agent": agent_name,
            "user_query": row[
                "user_query"
            ],
            "expected_tools": "|".join(
                sorted(expected)
            ),
            "predicted_tools": "|".join(
                sorted(predicted)
            ),
            "exact_match": (
                expected == predicted
            ),
            "failed": failed,
        })

    result_df = pd.DataFrame(
        results
    )

    metrics = {
        "total_queries": len(
            result_df
        ),

        "exact_tool_accuracy": round(
            float(
                result_df[
                    "exact_match"
                ].mean()
            ) * 100,
            2,
        ),

        "failure_rate": round(
            float(
                result_df[
                    "failed"
                ].mean()
            ) * 100,
            2,
        ),
    }

    return result_df, metrics


# ============================================================
# NUMERIC EXTRACTION
# ============================================================

def _extract_numbers(
    text: str,
) -> list[str]:
    """
    Extract business metric values while ignoring
    IDs, dates, ranges, and numbered-list markers.
    """

    # Normalize Unicode spaces commonly used by
    # LLMs as thousands separators.
    text = text.replace(
        "\u202f",
        " ",
    )

    text = text.replace(
        "\u00a0",
        " ",
    )

    # Convert:
    # 7 659  -> 7659
    # 87 902 -> 87902
    text = re.sub(
        r"(?<=\d)\s+(?=\d{3}\b)",
        "",
        text,
    )

    # Remove long hexadecimal/alphanumeric IDs.
    text = re.sub(
        r"\b[a-fA-F0-9]{20,}\b",
        "",
        text,
    )

    # Remove dates:
    # 2018-03
    # 2018-03-01
    text = re.sub(
        r"\b\d{4}[--–]\d{2}"
        r"(?:[--–]\d{2})?\b",
        "",
        text,
    )

    # Remove day ranges:
    # 4-7 days
    # 8–14 days
    text = re.sub(
        r"\b\d+\s*[--–]\s*"
        r"\d+\s+days?\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove:
    # 15+ days
    text = re.sub(
        r"\b\d+\+\s+days?\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove numbered-list markers.
    text = re.sub(
        r"(?m)^\s*\d+\.\s+",
        "",
        text,
    )

    pattern = (
        r"(?<![\w])"
        r"[-+]?\d[\d,]*"
        r"(?:\.\d+)?"
        r"(?![\w])"
    )

    return re.findall(
        pattern,
        text,
    )


def _normalize_number(
    value: str,
) -> float:
    """Normalize a numeric string for comparison."""

    return float(
        value.replace(
            ",",
            "",
        )
    )


def _collect_evidence_numbers(
    value,
) -> list[float]:
    """Recursively collect numeric values from structured evidence."""

    numbers = []

    if isinstance(
        value,
        bool,
    ):
        return numbers

    if isinstance(
        value,
        (int, float),
    ):
        numbers.append(
            round(
                float(value),
                2,
            )
        )

    elif isinstance(
        value,
        dict,
    ):
        for item in value.values():
            numbers.extend(
                _collect_evidence_numbers(
                    item
                )
            )

    elif isinstance(
        value,
        list,
    ):
        for item in value:
            numbers.extend(
                _collect_evidence_numbers(
                    item
                )
            )

    return numbers


# ============================================================
# NUMERIC FAITHFULNESS
# ============================================================

def evaluate_numeric_faithfulness(
    final_answer: str,
    agent_results: dict,
) -> dict:
    """
    Check whether numbers appearing in the final answer
    are supported by specialist evidence.
    """

    evidence_numbers = set(
        _collect_evidence_numbers(
            agent_results
        )
    )

    answer_numbers = [
        round(
            _normalize_number(
                value
            ),
            2,
        )
        for value
        in _extract_numbers(
            final_answer
        )
    ]

    supported = []
    unsupported = []

    for number in answer_numbers:

        if number in evidence_numbers:
            supported.append(
                number
            )

        else:
            unsupported.append(
                number
            )

    total = len(
        answer_numbers
    )

    faithfulness_rate = (
        len(supported)
        / total
        * 100
        if total > 0
        else 100.0
    )

    return {
        "numbers_in_answer": total,
        "supported_numbers": len(
            supported
        ),
        "unsupported_numbers": (
            unsupported
        ),
        "numeric_faithfulness_rate": round(
            faithfulness_rate,
            2,
        ),
    }


# ============================================================
# GROUNDING EVALUATION
# ============================================================

def evaluate_grounding_questions(
    questions: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Run end-to-end numeric grounding evaluation."""

    from src.agents.graph import (
        retailops_graph,
    )

    results = []

    for query in questions[
        "user_query"
    ]:

        initial_state = {
            "user_query": query,
            "selected_agents": [],
            "agent_results": {},
            "evidence": [],
            "final_answer": None,
            "errors": [],
        }

        graph_result = (
            retailops_graph.invoke(
                initial_state
            )
        )

        faithfulness = (
            evaluate_numeric_faithfulness(
                final_answer=(
                    graph_result[
                        "final_answer"
                    ]
                ),
                agent_results=(
                    graph_result[
                        "agent_results"
                    ]
                ),
            )
        )

        results.append({
            "user_query": query,
            **faithfulness,
        })

        # Full graph execution uses Groq.
        _pace_groq_evaluation()

    result_df = pd.DataFrame(
        results
    )

    metrics = {
        "total_questions": len(
            result_df
        ),

        "average_numeric_faithfulness": round(
            float(
                result_df[
                    "numeric_faithfulness_rate"
                ].mean()
            ),
            2,
        ),

        "answers_with_unsupported_numbers": int(
            result_df[
                "unsupported_numbers"
            ]
            .apply(len)
            .gt(0)
            .sum()
        ),
    }

    return result_df, metrics


# ============================================================
# MULTI-AGENT EVALUATION
# ============================================================

def evaluate_multi_agent_scenarios(
    golden_set: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Evaluate end-to-end multi-agent routing and execution."""

    from src.agents.graph import (
        retailops_graph,
    )

    results = []

    for _, row in golden_set.iterrows():

        expected_agents = set(
            str(
                row[
                    "expected_agents"
                ]
            ).split("|")
        )

        initial_state = {
            "user_query": (
                row["user_query"]
            ),
            "selected_agents": [],
            "agent_results": {},
            "evidence": [],
            "final_answer": None,
            "errors": [],
        }

        try:
            graph_result = (
                retailops_graph.invoke(
                    initial_state
                )
            )

            selected_agents = set(
                graph_result[
                    "selected_agents"
                ]
            )

            executed_agents = set(
                graph_result[
                    "agent_results"
                ].keys()
            )

            routing_correct = (
                selected_agents
                == expected_agents
            )

            execution_correct = (
                executed_agents
                == expected_agents
            )

            answer_generated = bool(
                graph_result[
                    "final_answer"
                ]
            )

            no_errors = (
                len(
                    graph_result[
                        "errors"
                    ]
                )
                == 0
            )

        except Exception:
            selected_agents = set()
            executed_agents = set()

            routing_correct = False
            execution_correct = False
            answer_generated = False
            no_errors = False

        results.append({
            "user_query": (
                row["user_query"]
            ),
            "expected_agents": "|".join(
                sorted(
                    expected_agents
                )
            ),
            "selected_agents": "|".join(
                sorted(
                    selected_agents
                )
            ),
            "executed_agents": "|".join(
                sorted(
                    executed_agents
                )
            ),
            "routing_correct": (
                routing_correct
            ),
            "execution_correct": (
                execution_correct
            ),
            "answer_generated": (
                answer_generated
            ),
            "no_errors": no_errors,
            "failed": not no_errors,
        })

        # Full graph execution uses Groq.
        _pace_groq_evaluation()

    result_df = pd.DataFrame(
        results
    )

    metrics = {
        "total_scenarios": len(
            result_df
        ),

        "routing_accuracy": round(
            float(
                result_df[
                    "routing_correct"
                ].mean()
            ) * 100,
            2,
        ),

        "execution_accuracy": round(
            float(
                result_df[
                    "execution_correct"
                ].mean()
            ) * 100,
            2,
        ),

        "answer_generation_rate": round(
            float(
                result_df[
                    "answer_generated"
                ].mean()
            ) * 100,
            2,
        ),

        "failure_rate": round(
            float(
                result_df[
                    "failed"
                ].mean()
            ) * 100,
            2,
        ),

        "error_free_rate": round(
            float(
                result_df[
                    "no_errors"
                ].mean()
            ) * 100,
            2,
        ),
    }

    return result_df, metrics