"""Persistent local memory backed by SQLite. Data stays on this PC."""
from pathlib import Path
import sqlite3
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[1] / "memory" / "athen_memory.sqlite3"


class LocalMemory:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=5)

    def remember(self, content: str) -> str:
        content = " ".join((content or "").split()).strip()
        if not content:
            return "Tell me what you want me to remember."
        with self._connect() as db:
            db.execute("INSERT INTO memories(content, created_at) VALUES (?, ?)",
                       (content, datetime.now().isoformat(timespec="seconds")))
        return "I'll remember that on this PC."

    def recent(self, limit: int = 8) -> list[str]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT content FROM memories ORDER BY id DESC LIMIT ?",
                (max(1, min(int(limit), 30)),)
            ).fetchall()
        return [row[0] for row in rows]

    def clear(self) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM memories")
