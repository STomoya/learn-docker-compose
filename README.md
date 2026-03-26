# Learn Docker Compose

A hands-on, progressive workshop that takes you from running a single container to a production-ready multi-service stack with Docker Compose.

You'll build a **Legendary Loot Tracker** — a FastAPI app backed by PostgreSQL and Redis — and learn Docker Compose concepts one stage at a time.

## What You'll Build

```
                  ┌──────────────┐
    HTTP :80/:443 │    Caddy     │
   ──────────────►│ reverse proxy│
                  └──────┬───────┘
                         │ frontend_network
                  ┌──────▼───────┐
                  │   FastAPI    │
                  │     App      │
                  └──┬───────┬───┘
          backend_network (internal)
            ┌────┘           └────┐
     ┌──────▼───────┐    ┌───────▼──────┐
     │  PostgreSQL   │    │    Redis     │
     │  (storage)    │    │   (cache)    │
     └───────────────┘    └──────────────┘
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (with Compose v2)
- `curl` (for testing endpoints)

No Python installation required — everything runs inside containers.

## Workshop Stages

Each stage has its own directory with a `README.md` containing instructions and a `answer/` subdirectory with the solution.

| Stage | Topic | What You Learn |
|-------|-------|----------------|
| [1](stage1-basic-container/) | Basic Container | Write a `Containerfile`, build and run a single container |
| [2](stage2-compose-intro/) | Compose Intro | Define a service in `compose.yaml`, bind mounts |
| [3](stage3-add-postgres/) | Add PostgreSQL | Multi-service setup, environment variables, named volumes, `depends_on` |
| [4](stage4-add-redis/) | Add Redis | Cache-aside pattern, adding a third service |
| [5](stage5-healthchecks/) | Healthchecks | Service readiness checks, `condition: service_healthy` |
| [6](stage6-networks-and-proxy/) | Networks & Proxy | Custom networks, network isolation, Caddy reverse proxy |
| [7](stage7-production-ready/) | Production Ready | Resource limits, `.dockerignore`, security hardening |

## Getting Started

1. Clone this repository
2. Navigate to `stage1-basic-container/`
3. Read the `README.md` and follow the tasks
4. Check your work against the `answer/` directory
5. Move on to the next stage

```bash
git clone <repo-url>
cd learn-docker-compose/stage1-basic-container
cat README.md
```

## Tech Stack

- **App**: Python 3.12, FastAPI, SQLModel, redis-py
- **Database**: PostgreSQL 18
- **Cache**: Redis 8
- **Proxy**: Caddy 2
- **Package Manager**: uv

## Reference Solution

The `final/` directory contains the complete, fully-configured project with all stages applied. Use it as a reference if you get stuck.

```bash
cd final
cp .env.example .env
docker compose up --build
```

Then test:

```bash
# Add loot
curl -k -X POST https://localhost/loot/ \
  -H "Content-Type: application/json" \
  -d '{"item_name": "Dragon Scale", "rarity": "Legendary", "finder_name": "Hero"}'

# Get latest (first call hits DB, second call hits cache)
curl -k https://localhost/loot/latest

# List all
curl -k https://localhost/loot/
```

## Cleanup

To tear down containers and remove volumes for any stage:

```bash
docker compose down -v
```

## License

See [LICENSE](LICENSE) for details.
