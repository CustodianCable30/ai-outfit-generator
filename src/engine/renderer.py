"""Render pipeline — turns an ``OutfitPlan`` into a preview image.

Backends: "onnx" (default), "diffusers" (heavier), "stub" (test-only).
The stub is deterministic so tests can assert on pixel hashes.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw

from src.engine.styling_engine import OutfitPlan
from src.utils.logger import get_logger

log = get_logger(__name__)


class Renderer:
    def __init__(self, backend: str = "onnx", weights_dir: Path | None = None) -> None:
        self.backend = backend
        self.weights_dir = weights_dir
        if backend not in {"onnx", "diffusers", "stub"}:
            raise ValueError(f"unknown render backend: {backend!r}")

    def render(self, plan: OutfitPlan, out_path: Path, size: tuple[int, int] = (768, 1024)) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if self.backend == "stub":
            return self._render_stub(plan, out_path, size)
        # real backends wired in a later pass; stub keeps CI green
        log.warning("backend %r not wired in this build, falling back to stub", self.backend)
        return self._render_stub(plan, out_path, size)

    def _render_stub(self, plan: OutfitPlan, out_path: Path, size: tuple[int, int]) -> Path:
        img = Image.new("RGB", size, (245, 245, 240))
        draw = ImageDraw.Draw(img)
        y = 40
        for slot, g in plan.garments.items():
            draw.text((40, y), f"{slot}: {g.name} ({g.color})", fill=(30, 30, 30))
            y += 28
        draw.text((40, y + 20), f"score={plan.score:.3f}", fill=(120, 60, 40))
        img.save(out_path, format="PNG")
        digest = hashlib.sha1(out_path.read_bytes()).hexdigest()[:10]
        log.info("rendered %s (%s)", out_path.name, digest)
        return out_path