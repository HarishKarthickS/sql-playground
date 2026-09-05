from __future__ import annotations

from sql_playground.data.connection import Database

_SEED_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    town TEXT NOT NULL,
    account_opened TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS papers (
    sku TEXT PRIMARY KEY,
    mill TEXT NOT NULL,
    weight_gsm INTEGER NOT NULL,
    color TEXT NOT NULL,
    sheets_on_hand INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    issued_on TEXT NOT NULL,
    due_on TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'paid', 'void')),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS invoice_lines (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES invoices(id),
    description TEXT NOT NULL,
    paper_sku TEXT REFERENCES papers(sku),
    qty INTEGER NOT NULL,
    unit_cents INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES invoices(id),
    received_on TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    method TEXT NOT NULL
);

INSERT INTO customers (id, name, town, account_opened) VALUES
    (1, 'Mira Ellison', 'Port Providence', '2023-04-11'),
    (2, 'North Lamp Press', 'Kelpward', '2022-11-02'),
    (3, 'Jonah Reed', 'Harborwick', '2024-01-19'),
    (4, 'Cinder & Salt Books', 'Mast Point', '2021-08-30'),
    (5, 'Ada Voss', 'Port Providence', '2025-02-07');

INSERT INTO papers (sku, mill, weight_gsm, color, sheets_on_hand) VALUES
    ('FLAX-90', 'River Fen Mill', 90, 'flax', 4200),
    ('IVORY-120', 'Ashmead', 120, 'ivory', 1800),
    ('NIGHT-160', 'Blackwater', 160, 'night blue', 640),
    ('LEDGER-80', 'River Fen Mill', 80, 'pale sage', 9000),
    ('KRAFT-200', 'Oak Spine', 200, 'kraft', 1100);

INSERT INTO invoices (id, customer_id, issued_on, due_on, status, notes) VALUES
    (101, 1, '2026-06-02', '2026-07-02', 'paid', 'Chapbook covers, edition of 200.'),
    (102, 2, '2026-06-18', '2026-07-18', 'open', 'Quarterly house stock.'),
    (103, 4, '2026-07-01', '2026-07-31', 'paid', 'Endpapers for the salt-marsh series.'),
    (104, 3, '2026-07-22', '2026-08-22', 'open', 'Wedding suite, letterpress.'),
    (105, 5, '2026-08-09', '2026-09-09', 'open', 'Thesis signatures, sewn.'),
    (106, 2, '2026-08-14', '2026-09-14', 'void', 'Wrong mill specified; rewritten as 107.'),
    (107, 2, '2026-08-15', '2026-09-14', 'paid', 'Replacement for voided 106.');

INSERT INTO invoice_lines (id, invoice_id, description, paper_sku, qty, unit_cents) VALUES
    (1, 101, 'Cover stock, night blue', 'NIGHT-160', 220, 48),
    (2, 101, 'Text block, flax', 'FLAX-90', 2400, 6),
    (3, 101, 'Saddle stitch labor', NULL, 200, 35),
    (4, 102, 'Ledger sheets', 'LEDGER-80', 5000, 4),
    (5, 102, 'Ivory text', 'IVORY-120', 800, 9),
    (6, 103, 'Kraft endpapers', 'KRAFT-200', 400, 18),
    (7, 103, 'Flax interiors', 'FLAX-90', 1600, 6),
    (8, 104, 'Ivory invitations', 'IVORY-120', 180, 22),
    (9, 104, 'Night reply cards', 'NIGHT-160', 180, 19),
    (10, 104, 'Hand-set type hours', NULL, 12, 4500),
    (11, 105, 'Thesis signatures', 'FLAX-90', 3200, 6),
    (12, 105, 'Sewn binding labor', NULL, 8, 6200),
    (13, 106, 'Wrong mill lot (void)', 'KRAFT-200', 200, 18),
    (14, 107, 'Oak Spine kraft', 'KRAFT-200', 200, 18),
    (15, 107, 'Rush recut', NULL, 1, 2500);

INSERT INTO payments (id, invoice_id, received_on, amount_cents, method) VALUES
    (1, 101, '2026-06-28', 29720, 'cheque'),
    (2, 103, '2026-07-19', 16800, 'wire'),
    (3, 107, '2026-08-20', 6100, 'cash'),
    (4, 104, '2026-08-01', 20000, 'cheque');
"""


def ensure_seeded(db: Database) -> None:
    db.path.parent.mkdir(parents=True, exist_ok=True)
    with db.session() as conn:
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'invoices'"
        ).fetchone()
        if exists:
            return
        conn.executescript(_SEED_SQL)
