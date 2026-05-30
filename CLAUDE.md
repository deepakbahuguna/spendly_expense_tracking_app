# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a personal expense tracker web app. Built as a step-by-step tutorial project; `app.py` contains stub routes with comments indicating which step implements each feature (Steps 1–9).

## Commands

```bash
# Activate virtualenv (named .vnv, not .venv)
source .vnv/bin/activate

# Run dev server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py
```

## Architecture

- **`app.py`** — all Flask routes; no blueprints yet
- **`database/db.py`** — not yet implemented; will contain `get_db()`, `init_db()`, `seed_db()` for SQLite with `row_factory` and foreign keys enabled
- **`templates/`** — Jinja2 templates extending `base.html`; `base.html` includes the shared navbar and footer
- **`static/css/style.css`** and **`static/js/main.js`** — single CSS/JS files, no build step

## Key details

- SQLite is the database (not yet wired up); `database/db.py` is a placeholder for Step 1
- Virtual environment folder is `.vnv` (not `.venv`)
- Fonts: DM Serif Display (headings) + DM Sans (body), loaded from Google Fonts in `base.html`
- App runs on port 5001 to avoid conflicts with macOS AirPlay (5000)
