# How This Repo Is Organized

```
app/
├── __init__.py     # the app factory — creates the app, wires extensions, defines routes
├── models/         # what a table looks like and how it relates to others
├── controllers/     # the actual database logic (queries, joins, aggregation)
├── schemas/        # converts model objects to/from JSON
├── auth/           # JWT issuing (jwt.py) and role checks (roles.py)
└── utils/          # small, dependency-free helpers used across routes
```

Every request follows the same path:

**Route** (`app/__init__.py`) → **Controller** (`app/controllers/`) → **Model** (`app/models/`) → back out through **Schema** (`app/schemas/`).

The route's only jobs are: read the request, call a controller, shape the
response. It never talks to the database directly. That split means a
controller method can be tested on its own (no server needed), reused from
`seed.py` or another route, and the ORM/database can change later without
touching every route.

## Example: fetching paginated sessions

```
GET /sessions?page=2&per_page=10&genre=amapiano
```

1. `@jwt_required()` checks the token before the route body runs at all.
2. The route reads `page` / `per_page` / `genre` from the query string and
   calls `SessionController.get_all_sessions(...)`.
3. The controller runs `Session.query.filter(...).paginate(...)`.
4. `app/utils/helpers.py`'s `paginated_response()` wraps the result with
   `total` / `page` / `per_page` / `total_pages` metadata, and the route
   returns it as JSON.

## Where roles fit in

- `@jwt_required()` (from Flask-JWT-Extended) answers *"is this a valid token?"* — authentication.
- `@role_required("admin")` (`app/auth/roles.py`) answers *"is this specific user allowed to do this?"* — authorization.

Both decorators can stack on the same route — auth first (closest to the function), role check above it.

## Why `auth/` is separate from `utils/`

`app/auth/` holds anything specific to *identity and permission*: issuing
tokens, checking roles. `app/utils/` holds generic helpers that don't know
or care about auth — request validation, pagination formatting, email
format checks. Keeping them apart makes it obvious where to look when
you're debugging a 401/403 versus a 400.
