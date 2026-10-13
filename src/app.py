"""Bootstrap entry point for the desktop app.

Boots the Qt application, wires the main window, and hands off to the
styling engine. Run with ``python -m src.app`` or via the frozen exe.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.config.settings import load_settings
from src.services.wardrobe_store import WardrobeStore
from src.services.weight_fetcher import ensure_weights
from src.ui.main_window import MainWindow
from src.utils.logger import get_logger, configure_logging

log = get_logger(__name__)


def bootstrap() -> int:
    """Boot the app. Returns a process exit code."""
    settings = load_settings(Path("config/app.toml"))
    configure_logging(settings.log_level, settings.log_dir)
    log.info("booting ai-outfit-generator v%s", settings.version)

    store = WardrobeStore(settings.wardrobe_db)
    store.migrate()

    if settings.auto_fetch_weights:
        ensure_weights(settings.weights_dir)

    app = QApplication(sys.argv)
    app.setApplicationName("AI Outfit Generator")
    window = MainWindow(settings=settings, store=store)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(bootstrap())