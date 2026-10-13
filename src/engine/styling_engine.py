"""Core styling engine.

Given a wardrobe, a brief (occasion, weather, palette, formality), and a
user profile, produce a ranked list of ``OutfitPlan`` candidates. Pure
logic — no disk, no network, no Qt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from src.engine.scoring import score_outfit
from src.models.garment import Garment
from src.models.profile import UserProfile
from src.utils.logger import get_logger

log = get_logger(__name__)

SLOTS = ("top", "bottom", "outerwear", "shoes", "accessory")


@dataclass(slots=True)
class OutfitBrief:
    occasion: str = "casual"
    season: str = "all"
    temperature_c: int = 18
    palette: tuple[str, ...] = ()
    formality: float = 0.5  # 0 = pyjamas, 1 = black tie


@dataclass(slots=True)
class OutfitPlan:
    garments: dict[str, Garment] = field(default_factory=dict)
    score: float = 0.0
    rationale: str = ""


class StylingEngine:
    """Rank wardrobe combinations against a brief."""

    def __init__(self, profile: UserProfile) -> None:
        self._profile = profile

    def plan(self, wardrobe: Sequence[Garment], brief: OutfitBrief, limit: int = 5) -> list[OutfitPlan]:
        by_slot: dict[str, list[Garment]] = {s: [] for s in SLOTS}
        for g in wardrobe:
            if g.slot in by_slot:
                by_slot[g.slot].append(g)

        candidates: list[OutfitPlan] = []
        for top in by_slot["top"]:
            for bottom in by_slot["bottom"]:
                shoes = by_slot["shoes"][:3]
                for shoe in shoes:
                    plan = OutfitPlan(garments={"top": top, "bottom": bottom, "shoes": shoe})
                    plan.score, plan.rationale = score_outfit(plan, brief, self._profile)
                    candidates.append(plan)

        candidates.sort(key=lambda p: p.score, reverse=True)
        log.debug("engine produced %d candidates, top=%.3f", len(candidates), candidates[0].score if candidates else 0.0)
        return candidates[:limit]

    def explain(self, plan: OutfitPlan) -> Iterable[str]:
        yield from plan.rationale.split("; ")