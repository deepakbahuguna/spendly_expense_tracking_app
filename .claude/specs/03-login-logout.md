# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate and access protected areas of Spendly. This step upgrades the stub `GET /login` to a full `POST` handler that verifies credentials against the database, stores the user's identity in the Flask session, and updates the navbar in `base.html` to show context-appropriate links. Logout clears the session and redirects to the landing page. After this step the app has a complete auth lifecycle: register → login → logout.

## Depends on
- Step 01 — Database setup (`database/db.py`, `users` table)
- Step 02 — Registration (`POST /register`, `users` rows with hashed passwords)

## Routes
- `GET  /login`  — render login form; redirect to landing if already logged in — public
- `POST /login`  — validate credentials, set session, redirect to landing — public
- `GET  /logout` — clear session, redirect to landing — logged-in only

## Database changes
No database changes. The `users` table already has all required columns.

## Templates
- **Modify:** `templates/base.html` — update `<div class="nav-links">` to show `Sign out` link when `session.user_id` is set, otherwise show `Sign in` + `Get started`
- **No change:** `templates/login.html` — already has flash message block, `{{ error }}` display, and `<form method="POST" action="/login">` — fully ready

## Files to change
- `app.py`
  - Add `session` to the `flask` import line
  - Add `check_password_hash` to the `werkzeug.security` import line
  - Change `@app.route("/login")` to `@app.route("/login", methods=["GET", "POST"])`
  - Implement `login()` GET branch: redirect to `url_for('landing')` if `session.get("user_id")`, else render form
  - Implement `login()` POST branch: validate → query DB → check hash → set session → redirect or re-render
  - Replace the `/logout` stub with a real implementation: clear session, redirect to landing
  - Add a session guard to `register()`: if already logged in, redirect to `url_for('landing')`
- `templates/base.html`
  - Make nav links conditional on `session.get("user_id")`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug` and `flask` are already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys: store `session["user_id"]` (integer) and `session["user_name"]` (string) on successful login
- Validation order for POST /login: (1) both fields non-empty, (2) user found by email, (3) password matches — return a single generic error for steps 2 and 3: `"Invalid email or password."` (do not reveal whether the email exists)
- Always close DB connection in a `finally` block
- Logout must use `session.clear()`, not `session.pop()`
- After successful login redirect to `url_for('landing')` (a dashboard route will be added in a later step)
- After logout redirect to `url_for('landing')` with no flash message

## Definition of done
- [ ] `GET /login` renders the empty form when not logged in
- [ ] `GET /login` redirects to landing when already logged in
- [ ] `POST /login` with blank fields shows an error inline (no redirect)
- [ ] `POST /login` with unknown email shows `"Invalid email or password."` (does not expose whether email exists)
- [ ] `POST /login` with correct email but wrong password shows `"Invalid email or password."`
- [ ] `POST /login` with correct credentials sets `session["user_id"]` and `session["user_name"]` and redirects to landing
- [ ] `GET /logout` clears the session and redirects to landing
- [ ] After logout, `session["user_id"]` is no longer present
- [ ] Navbar shows `Sign in` + `Get started` when logged out
- [ ] Navbar shows `Sign out` (linked to `/logout`) when logged in
- [ ] `GET /register` redirects to landing when already logged in
- [ ] Demo seed user (`demo@spendly.com` / `demo123`) can log in successfully
