# Local Memory Setup

This starter works without memory. Add local memory only after the basic workflow discipline is useful.

The default local memory backend is Qdrant running in Docker Desktop, bound to `127.0.0.1` and protected by local API keys. Qdrant is the vector database; it does not decide what should be remembered. Workflows should still propose memory updates and wait for approval.

## What This Adds

- Docker Desktop runs the local Qdrant container.
- Qdrant stores approved vectors and metadata in a Docker volume.
- The repo keeps only templates and scripts.
- Real local keys live in `.env.qdrant`, which is ignored by Git.
- The morning script can verify that local memory is available.

## Prerequisites

1. Install Docker Desktop.
2. Start Docker Desktop and wait until the engine is running.
3. Confirm Compose is available:

   ```bash
   docker compose version
   ```

## 1. Create Local Env File

From the repo root:

```bash
cp templates/env/qdrant.env.example .env.qdrant
chmod 600 .env.qdrant
```

Generate two different local tokens:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Edit `.env.qdrant` and replace:

- `replace-with-random-write-token`
- `replace-with-random-read-only-token`

Keep the matching aliases aligned:

```text
QDRANT__SERVICE__API_KEY == QDRANT_API_KEY
QDRANT__SERVICE__READ_ONLY_API_KEY == QDRANT_READ_ONLY_API_KEY
```

## 2. Start Qdrant

```bash
docker compose up -d qdrant
```

Check the container:

```bash
docker compose ps
```

Qdrant should be reachable only from the local machine:

```text
127.0.0.1:6333 -> REST API
127.0.0.1:6334 -> gRPC API
```

## 3. Check Health

Load the local env file into the shell:

```bash
set -a
source .env.qdrant
set +a
```

Check Qdrant health:

```bash
curl -sS -H "api-key: ${QDRANT_API_KEY}" http://127.0.0.1:6333/healthz
```

## 4. Create The Collection

```bash
scripts/create_memory_collection.py
```

Default collection:

```text
manager_openbrain_memory_v1
```

Default vector profile:

```text
size: 384
distance: Cosine
```

This only creates an empty collection. It does not insert memory.

## 5. Verify Morning Startup

```bash
scripts/openbrain_morning_start.py --expect-memory
```

Expected outcome:

- Docker daemon: `PASS`
- Qdrant container: `PASS`
- Qdrant env: `PASS`
- Qdrant health: `PASS`
- Qdrant collection: `PASS`

## Daily Commands

Start:

```bash
docker compose up -d qdrant
```

Stop but keep data:

```bash
docker compose stop qdrant
```

View logs:

```bash
docker compose logs --tail=100 qdrant
```

Update image:

```bash
docker compose pull qdrant
docker compose up -d qdrant
```

## Destructive Reset

This removes the local Qdrant container and Docker volumes for this starter.

Only run it when you deliberately want to delete local memory data:

```bash
docker compose down -v
```

## Safety Notes

- Do not expose Qdrant to `0.0.0.0`.
- Do not commit `.env.qdrant`.
- Do not store raw credentials, broad raw exports, or sensitive customer data in memory.
- Prefer source pointers and approved summaries.
- Use the read-only token for search workflows where possible.
- Keep memory writes approval-gated.
- For remote or shared deployments, use proper TLS and a separate security review.

## References

- [Qdrant configuration](https://qdrant.tech/documentation/operations/configuration/) documents environment variable configuration and the `QDRANT__...` nested setting format.
- [Qdrant security](https://qdrant.tech/documentation/operations/security/) says self-deployed instances are not secure by default and recommends authentication plus binding local development to `127.0.0.1`.
- [Docker volumes](https://docs.docker.com/engine/storage/volumes/) documents named volumes as persistent storage that survives container removal unless the volume is deleted.
