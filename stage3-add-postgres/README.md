# Stage 3: Add a PostgreSQL Database

## Goal
Learn how to add a database service, use environment variables, named volumes, and `depends_on`.

## Background
The app now uses SQLModel to store loot items in PostgreSQL. You need to add a `postgres` service and wire it up.

## Files Provided
- `main.py` — Updated app that connects to PostgreSQL (no Redis yet)
- `pyproject.toml` — Updated with `psycopg` and `sqlmodel` dependencies
- `Containerfile` — Same as before
- `.env` — Environment variables for database connection

## Tasks

1. **Review the `.env` file** — it contains database credentials used by both the app and PostgreSQL.

2. **Update `compose.yaml`** to add a `postgres` service:
   - Use the image `docker.io/library/postgres:18.3-trixie`
   - Set `container_name: postgres`
   - Pass environment variables: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (use `${VAR:-default}` syntax to read from `.env`)
   - Add a named volume `postgres_data` mounted to `/var/lib/postgresql`
   - Define the volume in the top-level `volumes:` section

3. **Update the `app` service:**
   - Add `env_file: - .env` so the app can read database connection settings
   - Add `depends_on: - postgres` so the database starts first

4. **Run and test:**
   ```bash
   docker compose up --build
   curl -X POST http://localhost:8000/loot/ \
     -H "Content-Type: application/json" \
     -d '{"item_name": "Dragon Scale", "rarity": "Legendary", "finder_name": "Hero"}'
   curl http://localhost:8000/loot/
   ```

## Hints
- The `${VAR:-default}` syntax in compose.yaml reads from the shell environment (or `.env`), falling back to the default value.
- `depends_on: - postgres` ensures Docker starts the postgres container before the app. Note: this only waits for the container to *start*, not for PostgreSQL to be *ready*. You may need to retry the first request if the database isn't ready yet. We'll fix this properly in a later stage with healthchecks.
