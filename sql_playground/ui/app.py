from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template, request

from sql_playground.data.connection import Database, default_paths
from sql_playground.data.executor import run_sql
from sql_playground.data.schema import inspect_schema
from sql_playground.data.seed import ensure_seeded
from sql_playground.domain.errors import QueryError

ROOT = Path(__file__).resolve().parents[2]
BINDERY_PATH, SAVED_PATH = default_paths(ROOT / "data")


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    bindery = Database(BINDERY_PATH)
    ensure_seeded(bindery)

    @app.route("/")
    def desk() -> str:
        tables = inspect_schema(bindery)
        return render_template(
            "desk.html",
            tables=tables,
            default_sql=_starter_sql(),
        )

    @app.post("/run")
    def run() -> str:
        sql = request.form.get("sql", "")
        try:
            result = run_sql(bindery, sql)
        except QueryError as exc:
            return render_template("partials/results.html", error=str(exc), result=None)
        tables = inspect_schema(bindery)
        schema_html = render_template("partials/schema.html", tables=tables)
        results_html = render_template("partials/results.html", error=None, result=result)
        return results_html + f'<div id="folio-refresh" hx-swap-oob="innerHTML:.gutter-body">{schema_html}</div>'

    return app


def _starter_sql() -> str:
    return (
        "SELECT c.name, i.id AS invoice, i.status,\n"
        "       SUM(l.qty * l.unit_cents) AS total_cents\n"
        "FROM invoices i\n"
        "JOIN customers c ON c.id = i.customer_id\n"
        "JOIN invoice_lines l ON l.invoice_id = i.id\n"
        "GROUP BY c.name, i.id, i.status\n"
        "ORDER BY i.id;"
    )


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port=5055, debug=True)


if __name__ == "__main__":
    main()
