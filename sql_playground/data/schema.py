from __future__ import annotations

from sql_playground.data.connection import Database
from sql_playground.domain.models import ColumnInfo, TableInfo


def inspect_schema(db: Database) -> tuple[TableInfo, ...]:
    with db.session() as conn:
        names = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        tables: list[TableInfo] = []
        for name in names:
            pragma = conn.execute(f"PRAGMA table_info({_quote_ident(name)})").fetchall()
            columns = tuple(
                ColumnInfo(
                    name=row["name"],
                    col_type=row["type"] or "ANY",
                    not_null=bool(row["notnull"]),
                    primary_key=bool(row["pk"]),
                )
                for row in pragma
            )
            count = conn.execute(f"SELECT COUNT(*) FROM {_quote_ident(name)}").fetchone()[0]
            tables.append(TableInfo(name=name, columns=columns, row_count=int(count)))
        return tuple(tables)


def _quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'
