# Stage 2: Your First Docker Compose File

## Goal
Learn how to define a service in `compose.yaml` and use `docker compose up` instead of manual `docker build` + `docker run`.

## Background
You already have a working `Containerfile` from Stage 1. Now wrap it in a `compose.yaml` so you can manage it more easily.

## Files Provided
- `main.py` — Same minimal FastAPI app from Stage 1
- `pyproject.toml` — Python dependencies
- `Containerfile` — The container image definition from Stage 1

## Tasks

1. **Create a `compose.yaml`** that defines a single service called `app`:
   - Uses `build:` to build from the `Containerfile` in the current directory
   - Maps port `8000` on the host to port `8000` in the container
   - Uses a bind mount to mount the current directory (`.`) to `/app` in the container
   - Excludes the `.venv` directory from the bind mount using an anonymous volume

2. **Run it:**
   ```bash
   docker compose up --build
   ```

3. **Test it:**
   ```bash
   curl http://localhost:8000/loot/latest
   ```

4. **Stop it:**
   ```bash
   docker compose down
   ```

## Hints
- The `build.dockerfile` key specifies which file to use (e.g., `Containerfile`).
- The `build.context` key specifies the build context directory (`.`).
- To exclude `.venv` from the bind mount, add `/app/.venv` as a separate anonymous volume. This prevents the host's `.venv` from overriding the container's.
