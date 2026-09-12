import json
import sqlite3
from pathlib import Path
from typing import List, Dict


DB_PATH = Path("moodmirror.db")


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    features_json TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def save_entry(
        self,
        user_id: str,
        text: str,
        features: Dict[str, float],
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO entries (
                    user_id,
                    text,
                    features_json
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    text,
                    json.dumps(features),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_entries(self, user_id: str) -> List[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    user_id,
                    text,
                    features_json,
                    created_at
                FROM entries
                WHERE user_id = ?
                ORDER BY id ASC
                """,
                (user_id,),
            ).fetchall()

        entries = []

        for row in rows:
            features = json.loads(row[3])

            entry = {
                "id": row[0],
                "user_id": row[1],
                "text": row[2],
                "created_at": row[4],
            }

            entry.update(features)
            entries.append(entry)

        return entries