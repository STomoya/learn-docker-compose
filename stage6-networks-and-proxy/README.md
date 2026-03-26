# Stage 6: Custom Networks and Caddy Reverse Proxy

## Goal
Learn how to isolate services using custom Docker networks and add a reverse proxy with Caddy.

## Background
Right now all services share the default network, meaning any container can talk to any other. In production you want to separate concerns:
- A `backend_network` (internal, no internet access) for app ↔ postgres ↔ redis communication
- A `frontend_network` for caddy ↔ app communication, exposed to the outside

Caddy acts as a reverse proxy, forwarding HTTP requests to the app. The app no longer exposes its port directly.

## Files Provided
- `main.py`, `pyproject.toml`, `Containerfile`, `.env`, `.python-version` — Same as Stage 4
- `Caddyfile` — Caddy reverse proxy configuration

## Tasks

1. **Review the `Caddyfile`** — it proxies requests from `localhost` to the app at `172.100.0.10:8000`.

2. **Define two custom networks** in `compose.yaml`:
   - `backend_network`: bridge driver, `internal: true` (no external access), subnet `10.0.1.0/24`
   - `frontend_network`: bridge driver, subnet `172.100.0.0/24`

3. **Assign static IPs to services:**
   - `app`: `10.0.1.10` on backend, `172.100.0.10` on frontend
   - `postgres`: `10.0.1.20` on backend only
   - `redis`: `10.0.1.30` on backend only

4. **Add a `caddy` service:**
   - Use image `docker.io/library/caddy:2.11.2-alpine`
   - Set `container_name: caddy_proxy`
   - Map ports `80:80` and `443:443`
   - Bind mount the `Caddyfile` to `/etc/caddy/Caddyfile`
   - Add named volumes for `caddy_logs`, `caddy_data`, and `caddy_config`
   - Connect to `frontend_network` with IP `172.100.0.20`
   - Set `depends_on: - app`

5. **Remove the `ports` mapping from the `app` service** — Caddy handles external traffic now.

6. **Test:**
   ```bash
   docker compose up --build
   # Add data
   curl -k -X POST https://localhost/loot/ -H "Content-Type: application/json" -d '{"item_name": "Dragon Scale", "rarity": "Legendary", "finder_name": "Hero"}'
   # Access through Caddy on port 443
   curl -k https://localhost/loot/latest
   ```

## Hints
- `internal: true` on a network means containers on it cannot reach the internet. This is a security best practice for database networks.
- The `ipam` config block defines subnet and gateway for each network.
- Caddy automatically handles HTTPS with self-signed certs for `localhost`.
