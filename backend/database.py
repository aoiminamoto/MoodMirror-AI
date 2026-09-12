import sqlite3
from pathlib import Path
from typing import Dict, List

DB_PATH = Path("moodmirror.db")

FEATURE_COLUMNS = [
    "word_count",
    "lexical_diversity",
    "avg_sentence_length",
    "question_ratio",
    "exclamation_ratio",
    "future_orientation",
    "uncertainty",
    "action_orientation",
]


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                word_count REAL NOT NULL,
                lexical_diversity REAL NOT NULL,
                avg_sentence_length REAL NOT NULL,
                question_ratio REAL NOT NULL,
                exclamation_ratio REAL NOT NULL,
                future_orientation REAL NOT NULL,
                uncertainty REAL NOT NULL,
                action_orientation REAL NOT NULL
            )
            """
        )


def save_entry(user_id: str, text: str, features: Dict[str, float]) -> int:
    init_db()
    values = [features[name] for name in FEATURE_COLUMNS]
    placeholders = ", ".join(["?"] * (2 + len(FEATURE_COLUMNS)))
    columns = ", ".join(["user_id", "text", *FEATURE_COLUMNS])

    with get_connection() as conn:
        cursor = conn.execute(
            f"INSERT INTO entries ({columns}) VALUES ({placeholders})",
            [user_id, text, *values],
        )
        return int(cursor.lastrowid)


def get_user_entries(user_id: str) -> List[dict]:
    init_db()
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM entries WHERE user_id = ? ORDER BY created_at ASC, id ASC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]
