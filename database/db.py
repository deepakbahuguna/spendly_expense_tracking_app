import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123", method="pbkdf2:sha256"))
    )
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    expenses = [
        (user_id, 250.00,  "Food",          "2026-05-01", "Groceries"),
        (user_id, 120.50,  "Transport",     "2026-05-03", "Uber rides"),
        (user_id, 1800.00, "Bills",         "2026-05-05", "Electricity bill"),
        (user_id, 600.00,  "Health",        "2026-05-08", "Doctor visit"),
        (user_id, 350.00,  "Entertainment", "2026-05-10", "Netflix + movie"),
        (user_id, 890.00,  "Shopping",      "2026-05-14", "Clothes"),
        (user_id, 75.00,   "Food",          "2026-05-18", "Restaurant"),
        (user_id, 200.00,  "Other",         "2026-05-20", "Miscellaneous"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()
