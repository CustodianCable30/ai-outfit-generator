"""Feature handlers. Register new handlers in HANDLER_REGISTRY."""
from src.handlers.base_handler import BaseHandler
from src.handlers.daily_outfit_handler import DailyOutfitHandler
from src.handlers.occasion_handler import OccasionHandler
from src.handlers.palette_handler import PaletteHandler
from src.handlers.wardrobe_handler import WardrobeHandler

HANDLER_REGISTRY: dict[str, type[BaseHandler]] = {
    "daily": DailyOutfitHandler,
    "occasion": OccasionHandler,
    "palette": PaletteHandler,
    "wardrobe": WardrobeHandler,
}

__all__ = ["HANDLER_REGISTRY", "BaseHandler"]