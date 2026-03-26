# Stage 4: Add Redis Caching

## Goal
Learn how to add a second backing service (Redis) and implement a cache-aside pattern.

## Background
The app now uses Redis to cache the latest loot item. On the first request, it reads from PostgreSQL and stores the result in Redis. Subsequent requests are served from cache until it expires or is invalidated.

## Files Provided
- `main.py` — Updated app with Redis caching logic
- `pyproject.toml` — Updated with `redis` dependency
- `Containerfile`, `.env`, `.python-version` — Same as before

## Tasks

1. **Update `.env`** to add `REDIS_HOST=redis`.

2. **Add a `redis` service** to `compose.yaml`:
   - Use the image `docker.io/library/redis:8.6.1-trixie`
   - Set `container_name: redis_cache`
   - Override the default command: `redis-server --save 60 1 --loglevel warning`
   - Add a named volume `redis_data` mounted to `/data`

3. **Update the `app` service:**
   - Add `redis` to `depends_on`

4. **Run and test the cache-aside pattern:**
   ```bash
   docker compose up --build

   # Add some loot
   curl -X POST http://localhost:8000/loot/ \
     -H "Content-Type: application/json" \
     -d '{"item_name": "Phoenix Feather", "rarity": "Legendary", "finder_name": "Mage"}'

   # First call — should say "database"
   curl http://localhost:8000/loot/latest

   # Second call — should say "cache (lightning fast!)"
   curl http://localhost:8000/loot/latest
   ```

## Hints
- The `--save 60 1` flag tells Redis to persist data to disk every 60 seconds if at least 1 key changed.
- Don't forget to declare `redis_data` in the top-level `volumes:` section.
- You might notice the app sometimes crashes on startup because PostgreSQL or Redis isn't ready yet. We'll fix this in the next stage with healthchecks.
