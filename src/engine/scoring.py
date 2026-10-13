"""Scoring heuristics for outfit plans.

Blends palette match, formality delta, weather fit, and profile affinity
into a single [0, 1] score. Weights come from config; defaults are sane.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from src.models.profile import UserProfile

if TYPE_CHECKING:
    from src.engine.styling_engine import OutfitBrief, OutfitPlan

W_PALETTE = 0.42
W_FORMALITY = 0.31
W_WEATHER = 0.27


def _palette_match(plan: "OutfitPlan", brief: "OutfitBrief") -> float:
    if not brief.palette:
        return 0.5
    hits = 0
    total = 0
    for g in plan.garments.values():
        total += 1
        if g.color.lower() in {p.lower() for p in brief.palette}:
            hits += 1
    return hits / total if total else 0.0


def _formality_delta(plan: "OutfitPlan", brief: "OutfitBrief") -> float:
    avg = sum(g.formality for g in plan.garments.values()) / max(len(plan.garments), 1)
    return max(0.0, 1.0 - abs(avg - brief.formality))


def _weather_fit(plan: "OutfitPlan", brief: "OutfitBrief") -> float:
    warmth = sum(g.warmth for g in plan.garments.values()) / max(len(plan.garments), 1)
    # 0 warm → 30C ideal; 1 warm → -5C ideal
    ideal = 30 - (warmth * 35)
    return max(0.0, 1.0 - abs(ideal - brief.temperature_c) / 25.0)


def score_outfit(plan: "OutfitPlan", brief: "OutfitBrief", profile: UserProfile) -> tuple[float, str]:
    p = _palette_match(plan, brief)
    f = _formality_delta(plan, brief)
    w = _weather_fit(plan, brief)
    total = p * W_PALETTE + f * W_FORMALITY + w * W_WEATHER
    # profile affinity nudge
    if profile.favorite_colors:
        fav = {c.lower() for c in profile.favorite_colors}
        if any(g.color.lower() in fav for g in plan.garments.values()):
            total = min(1.0, total + 0.05)
    rationale = f"palette={p:.2f}; formality={f:.2f}; weather={w:.2f}"
    return round(total, 4), rationale