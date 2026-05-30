# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. This step adds the `POST /register` handler, input validation, password hashing, and a database insert. It also sets `app.secret_key` and wires up `flask.flash` so the app is ready for session-based messaging in the next step (Login). On success the user is redirected to `/login` with a flash message; on failure `register.html` is re-rendered with an inline error.

## Depends on
- Step 01 — Database setup (`database/db.py` with `get_db()`, `init_db()`, `seed_db()` and the `users` table)

## Routes
- `GET  /register` — render empty registration form — public
- `POST /register` — validate input, insert user, redirect to login — public

## Database changes
No database changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already exists from Step 01.

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}` and `{% if error %}`; add a `{% with messages %}` block above the form to display flashed success messages from the login redirect (only needed if you want the "Account created" banner to show on the login page — see note in implementation rules)

## Files to change
- `app.py`
  - Add `secret_key` to app config (use `os.urandom(24)` or a fixed dev string)
  - Add imports: `request`, `redirect`, `url_for`, `flash`, `session` from `flask`; `generate_password_hash` from `werkzeug.security`
  - Change `@app.route("/register")` to `@app.route("/register", methods=["GET", "POST"])`
  - Implement POST handler logic (validate → insert → redirect or re-render)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug` is already installed as a Flask dependency.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Hash passwords with `werkzeug.security.generate_password_hash` using `method="pbkdf2:sha256"`
- Use CSS variables — never hardcode hex values in any new styles
- All templates extend `base.html`
- Validation order: (1) all fields present and non-empty, (2) password ≥ 8 characters, (3) email not already registered — return the first error encountered
- On duplicate email use `SELECT` to check before `INSERT`; do not catch `IntegrityError` as the primary duplicate guard
- On successful registration: `flash("Account created — please sign in.", "success")` then `redirect(url_for("login"))`
- On validation failure: `return render_template("register.html", error="…")` — do not redirect
- `app.secret_key` must be set before any `flash()` call; place it immediately after `app = Flask(__name__)`
- Always close the DB connection in a `finally` block (or use a `with` statement if preferred)

## Definition of done
- [ ] `GET /register` renders the form with no errors
- [ ] Submitting blank fields shows "All fields are required." inline error
- [ ] Submitting a password shorter than 8 characters shows "Password must be at least 8 characters." inline error
- [ ] Submitting a duplicate email shows "An account with that email already exists." inline error
- [ ] Submitting valid name / email / password inserts a row into `users` with a hashed (not plain-text) password
- [ ] After successful registration the browser is redirected to `/login`
- [ ] A flash success message is visible on the login page after redirect
- [ ] The demo seed user (`demo@spendly.com`) still exists after registration of a second user
- [ ] App starts without errors (`python app.py`)
