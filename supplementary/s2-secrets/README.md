# Supplementary 2: Secrets Management

## Goal
Learn how to use Docker Compose secrets to handle sensitive data instead of passing everything through environment variables.

## Background
Throughout the workshop, database credentials have been stored in a `.env` file and injected as environment variables. This works, but has downsides:

- Environment variables are visible in `docker inspect` output
- They can leak into logs, error reports, and child processes
- Any process inside the container can read them

Docker Compose secrets provide a more secure alternative. Secrets are mounted as files inside the container at `/run/secrets/<name>`, readable only by the service that declares them. They never appear in `docker inspect` or process listings.

## Tasks

1. **Create secret files** containing sensitive values:
   ```bash
   echo "admin" > secrets/db_user.txt
   echo "password" > secrets/db_password.txt
   echo "myapp" > secrets/db_name.txt
   ```

2. **Define secrets in `compose.yaml`** using the top-level `secrets:` key:
   ```yaml
   secrets:
     db_user:
       file: ./secrets/db_user.txt
     db_password:
       file: ./secrets/db_password.txt
     db_name:
       file: ./secrets/db_name.txt
   ```

3. **Grant the `app` service access** to the secrets:
   ```yaml
   services:
     app:
       secrets:
         - db_user
         - db_password
         - db_name
   ```

4. **Grant the `postgres` service access** and use `POSTGRES_*_FILE` environment variables:
   ```yaml
   services:
     postgres:
       secrets:
         - db_user
         - db_password
         - db_name
       environment:
         POSTGRES_USER_FILE: /run/secrets/db_user
         POSTGRES_PASSWORD_FILE: /run/secrets/db_password
         POSTGRES_DB_FILE: /run/secrets/db_name
   ```
   The official PostgreSQL image supports `_FILE` suffixed env vars — it reads the secret from the file path instead of the value directly.

5. **Test it:**
   ```bash
   docker compose up --build

   # Verify secrets are mounted
   docker compose exec app ls /run/secrets/

   # Verify env vars don't contain passwords
   docker compose exec app env | grep POSTGRES

   # Verify the app still works
   curl -k -X POST https://localhost/loot/ \
     -H "Content-Type: application/json" \
     -d '{"item_name": "Secret Scroll", "rarity": "Legendary", "finder_name": "Rogue"}'
   curl -k https://localhost/loot/latest
   ```

## Hints
- Secrets are mounted read-only at `/run/secrets/<name>` by default.
- The `_FILE` convention is supported by many official Docker images (PostgreSQL, MySQL, MariaDB). Always check the image docs.
- For local development, file-based secrets are fine. In Docker Swarm or production, you'd use `external: true` secrets managed by the orchestrator.
- Add `secrets/` to your `.gitignore` so secret files are never committed.
- The fallback pattern in `read_secret()` lets the same code work both with secrets (production) and plain env vars (development).
