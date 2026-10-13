"""Base class for feature handlers.

A handler receives a parsed user request and the app context, and returns
an ``OutfitPlan`` (or raises ``HandlerError``). Handlers do not touch Qt —
they are pure and testable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.engine.styling_engine import OutfitPlan


class HandlerError(RuntimeError):
    """Raised when a handler cannot satisfy a request."""


@dataclass(slots=True)
class HandlerContext:
    wardrobe: list
    profile: Any
    settings: Any


class BaseHandler(ABC):
    name: str = "base"

    @abstractmethod
    def handle(self, request: dict, ctx: HandlerContext) -> OutfitPlan:
        """Return a plan or raise HandlerError."""

    def _require(self, request: dict, key: str) -> Any:
        if key not in request:
            raise HandlerError(f"missing required field: {key!r}")
        return request[key]