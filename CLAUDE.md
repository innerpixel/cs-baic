# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read this first

**Open `ops/project.state.hybrid` after this file.** It is the live coordination state — current slice, loop, done log, open edges, patchlog. Coordination memory persists in `ops/`, not in this file or your session.

The codon files in `ops/` follow the L2.5 hybrid format from `csmcl.space/operating-agreements`. YAML frontmatter + structured body. Read them as compact state, not narrative.

## Coordination model

Two roles, one state file:

- **Coordinator (Opus session)** — defines slices, writes builder prompts (embedded inside slice codons), reviews completed work, updates `ops/project.state.hybrid`. Surfaces only judgment calls to the user.
- **Builder (IDE session, Sonnet ok)** — reads `ops/project.state.hybrid` + the current slice codon, executes that slice, commits, appends one PATCHLOG line to the slice and to project.state. Does not choose scope.
- **User** — opens sessions; makes judgment calls (taste, name, pricing); approves slices.

If you are operating as builder, your scope and prompt live inside the current slice codon's `## Builder prompt` block. Do not improvise scope. If you hit a blocker: stop, append a line to the slice's `OPEN EDGES`, commit what you have, report back.

## What this repository is

A product-definition + early-build repository for **Business Companion AI** — a private AI operations workspace for Romanian SMEs.

The product, when built:
- AI Inbox (classify + summarize + extract uploaded business documents)
- Ask My Company (RAG over uploaded docs only)
- Email Reply Assistant (drafts only — never auto-sends)
- Document Extraction (invoices, contracts, client requests)
- Human Approval + Audit Log

Guiding principle: **AI prepares. Humans approve.**

## Document map

`ops/` — live coordination state (read first):
- `ops/project.state.hybrid` — entry point. Current slice, done log, open edges, patchlog.
- `ops/rules.constraints.hybrid` — durable rules (tone, data, language, stack, palette, prompt hygiene, MVP exclusions). Anchored. Do not violate.
- `ops/slice-N.<name>.hybrid` — one per build slice. Scope · acceptance · builder prompt · state · patchlog.

`codocz/` — internal dev/reference docs (L1 narrative, written in Phase 0). Kept separate from any future user-facing product documentation.
- `codocz/romanian_sme_ai_companion_blueprint.md` — vision, modules, MVP scope. Start here for product context.
- `codocz/romanian_sme_ai_companion_project_control_pack.md` — One-Page Brief, MVP boundary, synthetic demo company "Atelier Nova SRL", Prompt Registry (§23.5), AI Evaluation Checklist, Pilot Discovery Script, Architecture Decision Log.
- `codocz/romanian_sme_ai_companion_technical_stack_decision_pack.md` — stack choices, monorepo layout, data model, processing pipeline. (Frontend = SvelteKit; Vue option preserved as historical context only.)
- `codocz/romanian_sme_ai_companion_prompt_pack.md` — 28 sequential prompts (strategy → runtime AI → outreach).
- `codocz/romanian_sme_ai_companion_promotion_go_to_market_pack.md` — GTM messaging, channel plan, post bank.
- `codocz/romanian_sme_ai_companion_diagrams.md` — Mermaid diagrams + diagram style guide.
- `codocz/romanian_sme_ai_companion_build_recommendation.md` — sections 11–18: practical "how do I start" notes.
- `codocz/romanian_sme_ai_companion_development_phases.md` — near-duplicate of blueprint; resync or delete rather than letting them drift.
- `brainstorm_unsorted/` — earlier draft blueprints. Superseded.

The reference docs do not change often. The codons in `ops/` change every session. When in doubt: codons are state, narrative docs are spec.

## Common operations

**Postgres (infra/):**
```sh
cd infra && docker compose up -d postgres
```

**API (apps/api/):**
```sh
cd apps/api && uv run alembic upgrade head
cd apps/api && uv run uvicorn app.main:app --reload   # :8000
cd apps/api && uv run python scripts/seed_demo.py      # seed 7-doc demo set (invoices + contract + accountant email)
cd apps/api && uv run python -m app.evals.run          # run eval harness (all fixtures × analyzers)
cd apps/api && uv run python -m app.evals.run --fixture invoice_lumina --analyzer invoice_extractor
```

**Frontend (apps/web/):**
```sh
cd apps/web && npm run dev    # :5173
cd apps/web && npm run build
cd apps/web && npm run check  # svelte-check
```

Stack: SvelteKit · Svelte 5 · TypeScript · Tailwind v4 · FastAPI · SQLAlchemy · Alembic · PostgreSQL
Routes: `/` · `/demo` · `/app/inbox` (live, API) · `/app/ask` (mock)
Mock data: `apps/web/src/lib/data/inbox.ts`
