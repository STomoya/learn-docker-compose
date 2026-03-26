# Stage 1: Build and Run a Single Container

## Goal
Learn how to write a `Containerfile` (Dockerfile) and build/run a single container for a Python application.

## Background
You are given a simple Python FastAPI application (`main.py`) that returns a hardcoded response. Your job is to containerize it.

## Files Provided
- `main.py` — A minimal FastAPI app
- `pyproject.toml` — Python project dependencies
- `.python-version` — Specifies Python 3.12

## Tasks

1. **Create a `Containerfile`** that:
   - Uses `debian:bookworm-slim` as the base image
   - Sets environment variables: `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`
   - Copies the `uv` package manager from `ghcr.io/astral-sh/uv:latest`
   - Installs Python 3.12 using `uv python install 3.12`
   - Copies `pyproject.toml` and installs dependencies with `uv sync`
   - Copies the application code
   - Exposes port 8000
   - Runs the app with: `uv run uvicorn main:app --host 0.0.0.0 --port 8000`

2. **Build the image:**
   ```bash
   docker build -f Containerfile -t loot-app .
   ```

3. **Run the container:**
   ```bash
   docker run -p 8000:8000 loot-app
   ```

4. **Test it:**
   ```bash
   curl http://localhost:8000/loot/latest
   ```

## Hints
- Look at the `UV_LINK_MODE=copy` environment variable — it helps `uv` work correctly inside containers.
- Use a two-step dependency install: first copy `pyproject.toml` and sync, then copy the rest. This leverages Docker layer caching.
