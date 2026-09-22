from dataclasses import dataclass
from typing import Callable

from src.evaluation.schemas import (
    EvaluationResult,
)


@dataclass(frozen=True)
class Evaluator:
    """Definition of a registered RetailOps evaluator."""

    name: str
    category: str
    description: str
    handler: Callable[..., EvaluationResult]


class EvaluationRegistry:
    """Registry for discovering and running evaluators."""

    def __init__(self):
        self._evaluators: dict[
            str,
            Evaluator,
        ] = {}

    def register(
        self,
        evaluator: Evaluator,
    ) -> None:
        """Register an evaluator."""

        if evaluator.name in self._evaluators:
            raise ValueError(
                f"Evaluator already registered: "
                f"{evaluator.name}"
            )

        self._evaluators[
            evaluator.name
        ] = evaluator

    def get(
        self,
        name: str,
    ) -> Evaluator:
        """Retrieve an evaluator by name."""

        if name not in self._evaluators:
            raise KeyError(
                f"Unknown evaluator: {name}"
            )

        return self._evaluators[
            name
        ]

    def list_evaluators(
        self,
        category: str | None = None,
    ) -> list[Evaluator]:
        """List evaluators, optionally filtered by category."""

        evaluators = list(
            self._evaluators.values()
        )

        if category is not None:
            evaluators = [
                evaluator
                for evaluator in evaluators
                if evaluator.category
                == category
            ]

        return evaluators

    def run(
        self,
        name: str,
        **kwargs,
    ) -> EvaluationResult:
        """Run a registered evaluator."""

        evaluator = self.get(
            name
        )

        return evaluator.handler(
            **kwargs
        )

    def __len__(self) -> int:
        return len(
            self._evaluators
        )