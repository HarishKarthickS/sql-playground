from __future__ import annotations

import time

from sql_playground.data.connection import Database
from sql_playground.domain.errors import QueryError
from sql_playground.domain.models import QueryResult

_SELECT_PREFIXES = ("select", "with", "pragma", "explain")


def run_sql(db: Database, sql: str) -> QueryResult:
    text = sql.strip().rstrip(";")
    if not text:
        raise QueryError("The page is blank. Write a statement before running it.")

    kind = _kind(text)
    started = time.perf_counter()
    try:
        with db.session() as conn:
            cursor = conn.execute(text)
            elapsed = (time.perf_counter() - started) * 1000
            if kind == "select":
                columns = tuple(d[0] for d in cursor.description or [])
                rows = tuple(tuple(row) for row in cursor.fetchall())
                return QueryResult(columns=columns, rows=rows, elapsed_ms=elapsed, kind="select")
            return QueryResult(
                columns=(),
                rows=(),
                elapsed_ms=elapsed,
                kind="write",
                rowcount=cursor.rowcount,
            )
    except Exception as exc:
        raise QueryError(str(exc)) from exc


def _kind(sql: str) -> str:
    head = sql.lstrip().split(None, 1)[0].lower()
    return "select" if head in _SELECT_PREFIXES else "write"
