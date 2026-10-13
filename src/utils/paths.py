"""Path safety helpers. All user-supplied paths go through safe_join."""
from __future__ import annotations

from pathlib import Path


class UnsafePathError(ValueError):
    """Raised when a path escapes its allowed root."""


def safe_join(root: Path, *parts: str) -> Path:
    root = root.resolve()
    candidate = root.joinpath(*parts).resolve()
    if root not in candidate.parents and candidate != root:
        raise UnsafePathError(f"path escapes root: {candidate} not under {root}")
    return candidate