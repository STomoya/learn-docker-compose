# Supplementary 1: Compose Overrides & Multiple Files

## Goal
Learn how to use `compose.override.yaml` and multiple Compose files to manage environment-specific configurations (dev vs prod).

## Background
In the main workshop, you built a single `compose.yaml` that mixes development conveniences (bind mounts, exposed debug ports) with production settings (resource limits, network isolation). In real projects, you want to separate these concerns.

Docker Compose automatically merges `compose.yaml` with `compose.override.yaml` if both exist. You can also explicitly specify multiple files with `-f` flags. Later values override earlier ones.

## Merge Rules

Understanding how Compose merges files is key:

- **Scalar values** (image, container_name): the override replaces the base value
- **Lists** (ports, volumes, environment): the override appends to the base list
- **Mappings** (deploy, healthcheck): the override is recursively merged

## Tasks

1. **Split `compose.yaml` into a base file** that contains only production settings:
   - Remove bind mounts from the `app` service (production uses the baked-in image)
   - Remove commented-out debug ports
   - Keep resource limits, healthchecks, networks, and all service definitions

2. **Create `compose.override.yaml`** with development-only settings:
   - Add the bind mount back to the `app` service (`.` → `/app`) with the `.venv` exclusion
   - Expose debug ports for postgres (`5432:5432`) and redis (`6379:6379`)
   - Remove resource limits from postgres and redis (so your dev machine isn't constrained)
   - Set the app command to use `--reload` for hot-reloading:
     ```yaml
     command: uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```

3. **Test the default (dev) behavior** — Compose auto-merges both files:
   ```bash
   docker compose up --build
   # Verify bind mount is active (edit main.py locally, see changes)
   # Verify debug ports are open
   curl http://localhost:8000/loot/latest
   ```

4. **Test production-only** — skip the override file:
   ```bash
   docker compose -f compose.yaml up --build
   # Verify no bind mount, no debug ports, resource limits active
   docker stats --no-stream
   ```

5. **Bonus: Create `compose.prod.yaml`** with production-specific additions:
   - Add `restart: unless-stopped` to all services
   - This can be used as: `docker compose -f compose.yaml -f compose.prod.yaml up -d`

## Hints
- `docker compose config` shows the final merged result — very useful for debugging.
- The override file only needs to specify the keys you want to change. Everything else is inherited from the base.
- When using `-f`, the auto-merge of `compose.override.yaml` is disabled. You must list all files explicitly.
- To verify which files Compose is using: `docker compose config --services` and check the output.
