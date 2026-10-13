"""Garment domain model."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict

VALID_SLOTS = {"top", "bottom", "outerwear", "shoes", "accessory"}


@dataclass(slots=True)
class Garment:
    name: str
    slot: str
    color: str
    warmth: float = 0.5
    formality: float = 0.5
    tags: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.slot not in VALID_SLOTS:
            raise ValueError(f"invalid slot: {self.slot!r}; expected one of {sorted(VALID_SLOTS)}")
        if not 0.0 <= self.warmth <= 1.0:
            raise ValueError("warmth must be in [0, 1]")
        if not 0.0 <= self.formality <= 1.0:
            raise ValueError("formality must be in [0, 1]")

    @classmethod
    def from_dict(cls, d: dict) -> "Garment":
        return cls(
            name=d["name"],
            slot=d["slot"],
            color=d["color"],
            warmth=float(d.get("warmth", 0.5)),
            formality=float(d.get("formality", 0.5)),
            tags=list(d.get("tags", [])),
            id=d.get("id", str(uuid.uuid4())),
        )

    @classmethod
    def from_row(cls, row) -> "Garment":
        import json
        return cls(
            name=row["name"],
            slot=row["slot"],
            color=row["color"],
            warmth=row["warmth"],
            formality=row["formality"],
            tags=json.loads(row["tags"]),
            id=row["id"],
        )

    def to_dict(self) -> dict:
        return asdict(self)