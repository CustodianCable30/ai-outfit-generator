"""Handler for the 'what do I wear today' flow."""
from __future__ import annotations

from datetime import date

from src.engine.styling_engine import OutfitBrief, OutfitPlan, StylingEngine
from src.handlers.base_handler import BaseHandler, HandlerContext, HandlerError


class DailyOutfitHandler(BaseHandler):
    name = "daily"

    def handle(self, request: dict, ctx: HandlerContext) -> OutfitPlan:
        if not ctx.wardrobe:
            raise HandlerError("wardrobe is empty — import some garments first")
        brief = OutfitBrief(
            occasion=request.get("occasion", "casual"),
            season=request.get("season", ctx.settings.default_season),
            temperature_c=int(request.get("temperature_c", 18)),
            palette=tuple(request.get("palette", ())),
            formality=float(request.get("formality", 0.4)),
        )
        engine = StylingEngine(ctx.profile)
        plans = engine.plan(ctx.wardrobe, brief, limit=1)
        if not plans:
            raise HandlerError(f"no viable outfit for {date.today().isoformat()}")
        return plans[0]