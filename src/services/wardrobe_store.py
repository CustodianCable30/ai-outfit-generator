"""SQLite-backed wardrobe persistence.

Threading: SQLite is opened with ``check_same_thread=False`` and every
write goes through ``self._lock``. Do not remove the lock without a
concurrency review — the Qt worker pool hits this from multiple threads.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from src.models.garment import Garment
from src.utils.logger import get_logger

log = get_logger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS garments (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slot TEXT NOT NULL,
    color TEXT NOT NULL,
    warmth REAL NOT NULL DEFAULT 0.5,
    formality REAL NOT NULL DEFAULT 0.5,
    tags TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_garments_slot ON garments(slot);
"""


class WardrobeStore:
    def __init__(self, db_path: Path) -> None:
        self._path = db_path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()

    def migrate(self) -> None:
        with self._lock:
            self._conn.executescript(SCHEMA)
            self._conn.commit()
        log.info("wardrobe schema ready at %s", self._path)

    def add(self, g: Garment) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO garments (id, name, slot, color, warmth, formality, tags) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (g.id, g.name, g.slot, g.color, g.warmth, g.formality, json.dumps(g.tags)),
            )
            self._conn.commit()

    def all(self) -> list[Garment]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM garments ORDER BY created_at DESC").fetchall()
        return [Garment.from_row(r) for r in rows]

    def close(self) -> None:
        with self._lock:
            self._conn.close()