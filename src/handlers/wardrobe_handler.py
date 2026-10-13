"""Handler for wardrobe CRUD-ish requests routed from the UI."""
from __future__ import annotations

from src.engine.styling_engine import OutfitPlan
from src.handlers.base_handler import BaseHandler, HandlerContext, HandlerError
from src.models.garment import Garment


class WardrobeHandler(BaseHandler):
    name = "wardrobe"

    def handle(self, request: dict, ctx: HandlerContext) -> OutfitPlan:
        action = self._require(request, "action")
        if action == "add":
            g = Garment.from_dict(self._require(request, "garment"))
            ctx.wardrobe.append(g)
            return OutfitPlan(garments={"added": g}, score=1.0, rationale="wardrobe add")
        if action == "list":
            return OutfitPlan(
                garments={f"item_{i}": g for i, g in enumerate(ctx.wardrobe[:10])},
                score=1.0,
                rationale=f"wardrobe has {len(ctx.wardrobe)} items",
            )
        raise HandlerError(f"unknown wardrobe action: {action!r}")