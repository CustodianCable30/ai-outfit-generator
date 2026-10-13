"""Download and verify model weights on first run.

Weights are fetched from the release CDN and verified against a SHA256
manifest shipped with the app. Never trust a downloaded blob without
checking the hash.
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

from src.utils.logger import get_logger

log = get_logger(__name__)

CDN_BASE = "https://cdn.ai-outfit-generator.dev/weights/v0.4"
MANIFEST_NAME = "manifest.sha256"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(weights_dir: Path) -> dict[str, str]:
    manifest = weights_dir / MANIFEST_NAME
    if not manifest.exists():
        return {}
    out: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, name = line.partition("  ")
        out[name.strip()] = digest.strip()
    return out


def ensure_weights(weights_dir: Path) -> Path:
    weights_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_manifest(weights_dir)
    for name, expected in manifest.items():
        target = weights_dir / name
        if target.exists() and _sha256(target) == expected:
            continue
        log.info("fetching weight %s", name)
        urllib.request.urlretrieve(f"{CDN_BASE}/{name}", target)
        got = _sha256(target)
        if got != expected:
            target.unlink(missing_ok=True)
            raise RuntimeError(f"weight {name} hash mismatch: {got} != {expected}")
    return weights_dir