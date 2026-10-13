"""Handler for occasion-targeted outfits (wedding, interview, date night)."""
from __future__ import annotations

from src.engine.styling_engine import OutfitBrief, OutfitPlan, StylingEngine
from src.handlers.base_handler import BaseHandler, HandlerContext, HandlerError

OCCASION_PRESETS: dict[str, dict] = {
    "interview": {"formality": 0.85, "palette": ("navy", "charcoal", "white")},
    "wedding": {"formality": 0.8, "palette": ("cream", "sage", "navy")},
    "date_night": {"formality": 0.55, "palette": ("black", "burgundy", "camel")},
    "gym": {"formality": 0.05, "palette": ()},
    "brunch": {"formality": 0.35, "palette": ("white", "olive", "tan")},
}


class OccasionHandler(BaseHandler):
    name = "occasion"

    def handle(self, request: dict, ctx: HandlerContext) -> OutfitPlan:
        occasion = self._require(request, "occasion")
        preset = OCCASION_PRESETS.get(occasion, {"formality": 0.5, "palette": ()})
        brief = OutfitBrief(
            occasion=occasion,
            season=request.get("season", ctx.settings.default_season),
            temperature_c=int(request.get("temperature_c", 18)),
            palette=tuple(request.get("palette") or preset["palette"]),
            formality=float(request.get("formality", preset["formality"])),
        )
        plans = StylingEngine(ctx.profile).plan(ctx.wardrobe, brief, limit=3)
        if not plans:
            raise HandlerError(f"no outfit matches occasion={occasion!r}")
        return plans[0]