from pathlib import Path

import joblib


def save_model(
    model,
    path: Path,
) -> None:
    """Save a trained ML model to disk."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        path,
    )


def load_model(
    path: Path,
):
    """Load a trained ML model from disk."""

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found: {path}"
        )

    return joblib.load(path)