# Supplementary 3: Compose Profiles

## Goal
Learn how to use `profiles` to group optional services that only start when explicitly requested.

## Background
Not every service needs to run all the time. During development you might want a database admin UI (pgAdmin) or a cache inspector (RedisInsight), but these shouldn't run in production. Compose profiles let you tag services as optional — they only start when you activate their profile.

Services without a `profiles` key always start. Services with `profiles` only start when you pass `--profile <name>`.

## Tasks

1. **Add a public facing network** for debug containers:
   ```yaml
   networks:
     debug_network:
       driver: bridge
   ```

2. **Add a `pgadmin` service** with the `debug` profile:
   ```yaml
   pgadmin:
     image: docker.io/dpage/pgadmin4:latest
     container_name: pgadmin
     profiles:
       - debug
     environment:
       PGADMIN_DEFAULT_EMAIL: admin@local.dev
       PGADMIN_DEFAULT_PASSWORD: admin
       PGADMIN_LISTEN_PORT: 5050
     ports:
       - "5050:5050"
     networks:
       backend_network:
         ipv4_address: 10.0.1.40
       debug_network:
     depends_on:
       postgres:
         condition: service_healthy
   ```

3. **Add a `redisinsight` service** with the `debug` profile:
   ```yaml
   redisinsight:
     image: docker.io/redis/redisinsight:latest
     container_name: redisinsight
     profiles:
       - debug
     ports:
       - "5540:5540"
     networks:
       backend_network:
         ipv4_address: 10.0.1.50
       debug_network:
     depends_on:
       redis:
         condition: service_healthy
   ```

3. **Test without the profile** — debug tools should not start:
   ```bash
   docker compose up --build
   docker compose ps
   # You should NOT see pgadmin or redisinsight
   ```

4. **Test with the debug profile:**
   ```bash
   docker compose --profile debug up --build
   docker compose ps
   # Now pgadmin and redisinsight should be running
   ```

5. **Access the debug tools:**
   - pgAdmin: http://localhost:5050 (login: `admin@local.dev` / `admin`)
   - RedisInsight: http://localhost:5540

6. **Tear down including profiled services:**
   ```bash
   docker compose --profile debug down
   ```

## Hints
- A service can belong to multiple profiles: `profiles: [debug, monitoring]`.
- `docker compose down` without `--profile` will not stop profiled services. Always include the profile flag when tearing down.
- You can activate multiple profiles at once: `--profile debug --profile monitoring`.
- Profiles are a clean alternative to commenting/uncommenting services in your compose file.
- The `depends_on` of a profiled service still works — Docker will use the already-running dependency, it won't start a second instance.
