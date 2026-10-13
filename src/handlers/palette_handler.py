"""Handler for palette-first requests ('build around this green')."""
from __future__ import annotations

from src.engine.styling_engine import OutfitBrief, OutfitPlan, StylingEngine
from src.handlers.base_handler import BaseHandler, HandlerContext, HandlerError


class PaletteHandler(BaseHandler):
    name = "palette"

    def handle(self, request: dict, ctx: HandlerContext) -> OutfitPlan:
        palette = self._require(request, "palette")
        if isinstance(palette, str):
            palette = [p.strip() for p in palette.split(",") if p.strip()]
        if not palette:
            raise HandlerError("palette is empty")
        brief = OutfitBrief(
            occasion=request.get("occasion", "casual"),
            season=request.get("season", ctx.settings.default_season),
            temperature_c=int(request.get("temperature_c", 18)),
            palette=tuple(palette),
            formality=float(request.get("formality", 0.5)),
        )
        plans = StylingEngine(ctx.profile).plan(ctx.wardrobe, brief, limit=1)
        if not plans:
            raise HandlerError("no outfit matches that palette")
        return plans[0]