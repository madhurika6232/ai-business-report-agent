from typing import Any, Literal

from pydantic import BaseModel, Field


EvaluationStatus = Literal[
    "pass",
    "fail",
    "warning",
]


class EvaluationMetric(BaseModel):
    """One measured evaluation metric."""

    name: str = Field(
        min_length=1,
    )

    value: float

    threshold: float | None = None

    status: EvaluationStatus

    details: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvaluationResult(BaseModel):
    """Standard result returned by one RetailOps evaluator."""

    evaluator: str = Field(
        min_length=1,
    )

    category: str = Field(
        min_length=1,
    )

    metrics: list[EvaluationMetric]

    passed: bool
    completed: bool = True

    sample_size: int = Field(
        ge=0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvaluationSuiteResult(BaseModel):
    """Combined result from multiple evaluators."""

    results: list[EvaluationResult]

    overall_score: float = Field(
        ge=0,
        le=100,
    )

    passed: bool

    total_evaluators: int = Field(
        ge=0,
    )