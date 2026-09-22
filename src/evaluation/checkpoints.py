import json
from pathlib import Path

from src.evaluation.schemas import (
    EvaluationResult,
)


CHECKPOINT_DIR = Path(
    "data/evaluation/checkpoints"
)


def save_evaluation_checkpoint(
    result: EvaluationResult,
) -> Path:
    """Persist one completed evaluator result."""

    if not result.completed:
        raise ValueError(
            "Cannot checkpoint an incomplete evaluation."
        )

    CHECKPOINT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        CHECKPOINT_DIR
        / f"{result.evaluator}.json"
    )

    path.write_text(
        json.dumps(
            result.model_dump(),
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path


def load_evaluation_checkpoint(
    evaluator: str,
) -> EvaluationResult:
    """Load one evaluator checkpoint."""

    path = (
        CHECKPOINT_DIR
        / f"{evaluator}.json"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Evaluation checkpoint not found: "
            f"{evaluator}"
        )

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    return EvaluationResult.model_validate(
        data
    )


def checkpoint_exists(
    evaluator: str,
) -> bool:
    """Return whether a checkpoint exists."""

    return (
        CHECKPOINT_DIR
        / f"{evaluator}.json"
    ).exists()


def list_evaluation_checkpoints() -> list[str]:
    """Return available evaluator checkpoint names."""

    if not CHECKPOINT_DIR.exists():
        return []

    return sorted(
        path.stem
        for path
        in CHECKPOINT_DIR.glob(
            "*.json"
        )
    )


def delete_evaluation_checkpoint(
    evaluator: str,
) -> bool:
    """Delete an evaluator checkpoint."""

    path = (
        CHECKPOINT_DIR
        / f"{evaluator}.json"
    )

    if not path.exists():
        return False

    path.unlink()

    return True