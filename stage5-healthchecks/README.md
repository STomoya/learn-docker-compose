# Stage 5: Healthchecks and Startup Order

## Goal
Learn how to add healthchecks to services and use `depends_on` conditions to ensure proper startup order.

## Background
In the previous stages, you may have noticed the app sometimes fails on startup because PostgreSQL or Redis isn't fully ready yet. A simple `depends_on` only waits for the container to *start* — not for the service inside it to be *ready*.

Docker healthchecks solve this. A healthcheck is a command that Docker runs periodically inside a container to determine if the service is healthy. Combined with `depends_on: condition: service_healthy`, Docker will wait until the dependency is actually ready before starting dependent services.

## Files Provided
- All files from Stage 4, including a `compose.yaml` without healthchecks

## Tasks

1. **Add a healthcheck to the `postgres` service:**
   - Test command: `pg_isready -U ${POSTGRES_USER:-admin} -d ${POSTGRES_DB:-myapp}`
   - Use the `CMD-SHELL` form so shell variable expansion works
   - Set `interval: 10s`, `timeout: 5s`, `retries: 5`

2. **Add a healthcheck to the `redis` service:**
   - Test command: `redis-cli ping`
   - Use the `CMD` form (array syntax)
   - Set `interval: 10s`, `timeout: 5s`, `retries: 5`

3. **Update `depends_on` in the `app` service** to use conditions:
   ```yaml
   depends_on:
     postgres:
       condition: service_healthy
     redis:
       condition: service_healthy
   ```

4. **Run and observe the startup sequence:**
   ```bash
   docker compose up --build
   ```
   Watch the logs — you should see Docker waiting for the healthchecks to pass before starting the app.

5. **Verify healthcheck status:**
   ```bash
   docker compose ps
   ```
   You should see `(healthy)` next to postgres and redis.

## Hints
- There are two forms for healthcheck test commands:
  - `CMD-SHELL`: runs through a shell, supports `${}` variable expansion. Example: `["CMD-SHELL", "pg_isready -U admin"]`
  - `CMD`: runs directly without a shell. Example: `["CMD", "redis-cli", "ping"]`
- `interval` is how often the check runs. `timeout` is how long to wait for a single check. `retries` is how many consecutive failures before marking unhealthy.
- Without healthchecks, `depends_on` only guarantees container start order, not service readiness. This is the most common cause of "connection refused" errors on startup.
