# Supplementary 4: Scaling & Replicas

## Goal
Learn how to run multiple instances of the app service and load balance across them with Caddy.

## Background
So far you've run a single instance of the FastAPI app. In production, you often want multiple replicas for redundancy and throughput. Docker Compose supports this with `deploy.replicas`.

However, scaling requires a few changes to the existing setup:
- Remove `container_name` from the app (each replica needs a unique name)
- Remove static IP assignments from the app (each replica needs its own IP)
- Update Caddy to use DNS-based service discovery instead of a hardcoded IP

## Starting Point

This directory contains all the files from the completed Stage 7 project. You'll modify `compose.yaml`, `Caddyfile`, and `main.py` as part of the tasks below.

## Tasks

1. **Remove static IPs and container_name from the `app` service.** Replace the network config with simple network membership:
   ```yaml
   services:
     app:
       networks:
         - backend_network
         - frontend_network
   ```

2. **Add `deploy.replicas`** to the app service:
   ```yaml
   services:
     app:
       deploy:
         replicas: 3
   ```

3. **Remove the bind mount from the `app` service** — bind mounts don't work well with replicas since all instances share the same files. The app code should be baked into the image:
   ```yaml
   # Remove these lines from app:
   # volumes:
   #   - type: bind
   #     source: .
   #     target: /app
   #   - /app/.venv
   ```

4. **Run and test:**
   ```bash
   docker compose up --build
   docker compose ps
   # You should see 3 app containers

   # Hit the endpoint multiple times — watch "served_by" change
   curl -k https://localhost/loot/latest
   curl -k https://localhost/loot/latest
   curl -k https://localhost/loot/latest
   ```

7. **Scale dynamically** without restarting:
   ```bash
   docker compose up -d --scale app=5 --no-recreate
   docker compose ps
   ```

## Hints
- Docker Compose's internal DNS resolves a service name to all container IPs for that service. Caddy (and most reverse proxies) use this for round-robin load balancing.
- `container_name` must be removed because it forces a single unique name — you can't have 3 containers all named `loot-app`.
- Static IPs must be removed for the same reason — each replica needs its own IP, and Docker assigns them automatically.
- The `--no-recreate` flag in `docker compose up --scale` avoids restarting existing containers.
- If you need sticky sessions (same user always hits the same replica), look into Caddy's `lb_policy` directive.
