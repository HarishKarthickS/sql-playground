# SQL Playground

A local SQLite desk for poking at a schema, running statements, and pinning the ones worth keeping. The seed is **Harbor Bindery**: customers, paper stock, invoices, line items, and payments — a ledger, not a tax product.

## Run it

From this folder, on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m sql_playground
```

Open [http://127.0.0.1:5055](http://127.0.0.1:5055). You should see a ruled job ticket, a folio of tables on the left, and a starter `SELECT` that totals each invoice.

- **Run page** (or Ctrl+Enter) prints a results grid.
- Bad SQL shows up as a red-ink blot, not a stack trace.
- **Pin** stores the current statement in `data/saved.sqlite`. Click a clipping to load it back.
- First launch creates `data/bindery.sqlite` from the seed. Delete that file and restart if you want a clean book.

## Layout

- `sql_playground/domain` — query results, saved queries, schema types
- `sql_playground/data` — SQLite, inspect, execute, seed
- `sql_playground/ui` — Flask + Jinja + HTMX desk

## Screenshot

![Harbor Bindery desk](docs/desk.png)
