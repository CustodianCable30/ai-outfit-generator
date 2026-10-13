"""User profile model — palette preferences, sizes, body notes."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class UserProfile:
    display_name: str = "anon"
    favorite_colors: list[str] = field(default_factory=list)
    avoided_colors: list[str] = field(default_factory=list)
    sizes: dict[str, str] = field(default_factory=dict)
    default_formality: float = 0.4

    def to_dict(self) -> dict:
        return {
            "display_name": self.display_name,
            "favorite_colors": list(self.favorite_colors),
            "avoided_colors": list(self.avoided_colors),
            "sizes": dict(self.sizes),
            "default_formality": self.default_formality,
        }