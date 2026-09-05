# SQL Playground

A local SQLite lab in a **composition notebook**: blue marble cover, red margin, college-ruled white pages. Type in Source Code Pro; titles in Patrick Hand. The seed is still **Harbor Bindery** (customers, paper stock, invoices, lines, payments) — the dataset, not the UI.

## Run it

From this folder, on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m sql_playground
```

Open [http://127.0.0.1:5055](http://127.0.0.1:5055). You should see a composition-book sticker, a table of contents on the left leaf, and a starter `SELECT` on the ruled page.

- **Run it** (or Ctrl+Enter) prints a results grid.
- Bad SQL shows up as a red-pen note, not a stack trace.
- **Save** stores the current statement in `data/saved.sqlite`. Click a margin note to load it back.
- First launch creates `data/bindery.sqlite` from the seed. Delete that file and restart if you want a clean notebook.

## Layout

- `sql_playground/domain` — query results, saved queries, schema types
- `sql_playground/data` — SQLite, inspect, execute, seed
- `sql_playground/ui` — Flask + Jinja + HTMX notebook

## Screenshot

![Composition notebook SQL desk](docs/desk.png)
