"""Main application window.

Thin shell over the handlers. All real logic lives in ``handlers/`` and
``engine/``. The window only wires widgets to handler calls.
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.handlers import HANDLER_REGISTRY
from src.handlers.base_handler import HandlerContext, HandlerError
from src.models.profile import UserProfile
from src.utils.logger import get_logger

log = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, settings, store) -> None:
        super().__init__()
        self._settings = settings
        self._store = store
        self._profile = UserProfile()
        self.setWindowTitle("AI Outfit Generator")
        self.resize(720, 560)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        layout.addWidget(QLabel("Occasion"))
        self._occasion = QComboBox()
        self._occasion.addItems(list(HANDLER_REGISTRY.keys()))
        layout.addWidget(self._occasion)

        layout.addWidget(QLabel("Palette (comma-separated)"))
        self._palette = QLineEdit()
        self._palette.setPlaceholderText("navy, cream, olive")
        layout.addWidget(self._palette)

        self