# Stage 7: Production Hardening

## Goal
Learn how to add resource limits, `.dockerignore`, and other production best practices to your Docker Compose project.

## Background
You now have a fully working multi-service application. This final stage adds the finishing touches that make it production-ready:
- Resource limits to prevent any single container from consuming all host resources
- A `.dockerignore` file to keep the build context small and avoid leaking secrets
- Commented-out debug ports for development convenience

## Files Provided
- All files from Stage 5 (the complete working project)

## Tasks

1. **Create a `.dockerignore` file** that excludes:
   - `.env` (secrets should not be baked into images)
   - `Caddyfile` (not needed inside the app image)
   - `docker-compose.yml` / `compose.yaml`
   - `.venv` (virtual environment)
   - `__pycache__`

2. **Add resource limits** to the `postgres` service using `deploy.resources`:
   - CPU limit: `1.0`
   - Memory limit: `1G`
   - Memory reservation: `512M`

3. **Add resource limits** to the `redis` service:
   - CPU limit: `0.5`
   - Memory limit: `512M`

4. **Comment out direct port mappings** on `postgres` and `redis` (they should only be accessible via the internal network). Add them as comments for development debugging:
   ```yaml
   # ports:
   #   - "5432:5432"
   ```

5. **Verify everything works:**
   ```bash
   docker compose up --build
   # Add data
   curl -k -X POST https://localhost/loot/ -H "Content-Type: application/json" -d '{"item_name": "Dragon Scale", "rarity": "Legendary", "finder_name": "Hero"}'
   # Access through Caddy on port 443
   curl -k https://localhost/loot/latest
   ```

6. **Inspect resource limits:**
   ```bash
   docker stats
   ```

## Trouble shooting

If you get an error message similar to `failed to create network stage7-production-ready_frontend_network: Error response from daemon: invalid pool request: Pool overlaps with other one on this address space` when building the image, you should delete the network that was created on stage6:

```bash
docker network remove stage6-networks-and-proxy_backend_network stage6-networks-and-proxy_frontend_network
```

## Hints
- `deploy.resources.limits` sets hard caps. `deploy.resources.reservations` sets guaranteed minimums.
- `.dockerignore` works like `.gitignore` — one pattern per line.
- You can verify `.dockerignore` is working by checking the image size before and after.

## Congratulations!
You've built a complete Docker Compose project from scratch, progressively adding:
1. ✅ A containerized Python app
2. ✅ Docker Compose orchestration
3. ✅ PostgreSQL with environment variables and volumes
4. ✅ Redis caching with persistence
5. ✅ Healthchecks and reliable startup order
6. ✅ Network isolation and a Caddy reverse proxy
7. ✅ Production hardening with resource limits

The `final/` directory contains the complete reference solution.
