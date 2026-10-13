"""TOML-backed application settings.

Loads ``config/app.toml``, applies env overrides, and returns an immutable
``Settings`` dataclass. Env vars win over the file so packaging can inject
paths at build time.
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_data_dir

APP_NAME = "ai-outfit-generator"


@dataclass(frozen=True, slots=True)
class Settings:
    version: str = "0.4.2"
    log_level: str = "INFO"
    log_dir: Path = field(default_factory=lambda: Path(user_data_dir(APP_NAME)) / "logs")
    wardrobe_db: Path = field(default_factory=lambda: Path(user_data_dir(APP_NAME)) / "wardrobe.db")
    weights_dir: Path = field(default_factory=lambda: Path(user_data_dir(APP_NAME)) / "weights")
    renders_dir: Path = field(default_factory=lambda: Path(user_data_dir(APP_NAME)) / "renders")
    auto_fetch_weights: bool = True
    max_wardrobe_items: int = 5000
    default_season: str = "all"
    render_backend: str = "onnx"  # "onnx" | "diffusers" | "stub"


def load_settings(path: Path) -> Settings:
    raw: dict = {}
    if path.exists():
        raw = tomllib.loads(path.read_text(encoding="utf-8"))

    def _env(key: str, default):
        val = os.environ.get(f"AIOG_{key.upper()}")
        return val if val is not None else default

    base = Settings(
        version=_env("version", raw.get("version", "0.4.2")),
        log_level=_env("log_level", raw.get("log_level", "INFO")),
        log_dir=Path(_env("log_dir", raw.get("log_dir", Settings().log_dir))),
        wardrobe_db=Path(_env("wardrobe_db", raw.get("wardrobe_db", Settings().wardrobe_db))),
        weights_dir=Path(_env("weights_dir", raw.get("weights_dir", Settings().weights_dir))),
        renders_dir=Path(_env("renders_dir", raw.get("renders_dir", Settings().renders_dir))),
        auto_fetch_weights=bool(raw.get("auto_fetch_weights", True)),
        max_wardrobe_items=int(raw.get("max_wardrobe_items", 5000)),
        default_season=raw.get("default_season", "all"),
        render_backend=raw.get("render_backend", "onnx"),
    )
    return base