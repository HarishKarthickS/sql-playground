from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ColumnInfo:
    name: str
    col_type: str
    not_null: bool
    primary_key: bool


@dataclass(frozen=True)
class TableInfo:
    name: str
    columns: tuple[ColumnInfo, ...]
    row_count: int


@dataclass(frozen=True)
class QueryResult:
    columns: tuple[str, ...]
    rows: tuple[tuple[object, ...], ...]
    elapsed_ms: float
    kind: str
    rowcount: int | None = None

    @property
    def is_tabular(self) -> bool:
        return self.kind == "select"

    @property
    def is_empty(self) -> bool:
        return self.is_tabular and len(self.rows) == 0


@dataclass
class SavedQuery:
    title: str
    sql: str
    id: int | None = None
    created_at: datetime | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
