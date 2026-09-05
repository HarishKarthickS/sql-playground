from __future__ import annotations

from datetime import datetime, timezone

from sql_playground.data.connection import Database
from sql_playground.domain.errors import QueryError
from sql_playground.domain.models import SavedQuery

_SCHEMA = """
CREATE TABLE IF NOT EXISTS saved_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    sql TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SavedQueryStore:
    def __init__(self, db: Database) -> None:
        self._db = db
        with db.session() as conn:
            conn.executescript(_SCHEMA)

    def list_all(self) -> tuple[SavedQuery, ...]:
        with self._db.session() as conn:
            rows = conn.execute(
                "SELECT id, title, sql, created_at FROM saved_queries ORDER BY id DESC"
            ).fetchall()
        return tuple(
            SavedQuery(
                id=row["id"],
                title=row["title"],
                sql=row["sql"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        )

    def add(self, title: str, sql: str) -> SavedQuery:
        title = title.strip()
        sql = sql.strip()
        if not title:
            raise QueryError("Give the clipping a short title.")
        if not sql:
            raise QueryError("There is nothing on the page to save.")
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        with self._db.session() as conn:
            cursor = conn.execute(
                "INSERT INTO saved_queries (title, sql, created_at) VALUES (?, ?, ?)",
                (title, sql, stamp),
            )
            query_id = int(cursor.lastrowid)
        return SavedQuery(id=query_id, title=title, sql=sql, created_at=datetime.fromisoformat(stamp))

    def get(self, query_id: int) -> SavedQuery | None:
        with self._db.session() as conn:
            row = conn.execute(
                "SELECT id, title, sql, created_at FROM saved_queries WHERE id = ?",
                (query_id,),
            ).fetchone()
        if row is None:
            return None
        return SavedQuery(
            id=row["id"],
            title=row["title"],
            sql=row["sql"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def delete(self, query_id: int) -> None:
        with self._db.session() as conn:
            conn.execute("DELETE FROM saved_queries WHERE id = ?", (query_id,))
