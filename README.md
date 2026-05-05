# Business Companion AI

Private AI operations workspace for Romanian SMEs — documents, invoices, emails, contracts, and company knowledge in one intelligent workspace.

## Run

**Postgres:**
```sh
cd infra
cp .env.example .env   # edit credentials and LLM key
docker compose up -d postgres
```

**API:**
```sh
cd apps/api
cp ../../infra/.env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
# → http://localhost:8000
```

**Frontend:**
```sh
cd apps/web
npm install
npm run dev
# → http://localhost:5173
```

**Seed demo invoices** (with API running):
```sh
cd apps/api
uv run python scripts/seed_invoices.py
```

## Routes

- `/` — homepage (product overview, pilot offer)
- `/demo` — demo workflow with Atelier Nova SRL (static mock data)
- `/app/inbox` — live AI inbox (fetches from API, upload + extract + approve)
- `/app/ask` — Ask My Company (static mock Q&A, RAG lands in slice-5)

## Stack

Frontend: SvelteKit · Svelte 5 · TypeScript · Tailwind v4  
Backend: FastAPI · SQLAlchemy · Alembic · Pydantic · uv  
Database: PostgreSQL 16  
LLM: OpenAI-compatible client (default: Mistral via API)

## Docs and coordination state

- `ops/project.state.hybrid` — current build slice and patchlog (start here)
- `ops/rules.constraints.hybrid` — durable constraints (palette, tone, data, stack)
- `codocz/` — product vision, MVP boundary, stack decisions, prompt registry

## Demo data

All data in `apps/web/src/lib/data/inbox.ts` is synthetic. Demo company: **Atelier Nova SRL** (Pitești, 12 employees). No real CUI, IBAN, name, or company data.
