# Business Companion AI — API

FastAPI backend for the Business Companion AI.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Docker (for Postgres)

## Run Postgres

```sh
cd infra
cp .env.example .env          # edit values as needed
docker compose up -d postgres
```

## Run the API

```sh
cd apps/api
cp ../../infra/.env.example .env   # edit values
uv sync
uv run alembic upgrade head        # run migrations
uv run uvicorn app.main:app --reload
```

API will be available at http://localhost:8000

Health check: `curl http://localhost:8000/api/health`

## Seed demo invoices

With the API running:

```sh
uv run python scripts/seed_invoices.py
```

## Run type checks

```sh
uv run pyright
```
