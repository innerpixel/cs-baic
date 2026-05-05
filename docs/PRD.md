# Business Companion AI — Product Requirements Document

**Status:** Living document — updated after each build slice  
**Last updated:** 2026-05-05 · Slice 3 complete  
**Build phase:** Phase 1 — MVP

---

## How to read this document

This document answers three questions:

1. **What is this product?** — purpose, who it is for, what it does
2. **What is built right now?** — what you can run and use today
3. **What is coming next?** — roadmap, by slice

Jump straight to [Current Build Status](#current-build-status) if you want to know what works today.

---

## What is Business Companion AI

**One sentence:** A private AI operations workspace that helps Romanian SMEs organize documents, invoices, emails, contracts, accountant communication, and company knowledge into clear next actions.

**The problem it solves:**

Romanian SMEs lose time inside scattered documents, repeated email threads, invoices, supplier messages, contracts, and accountant requests. The owner or office manager has to read everything, understand everything, and decide what to do next — manually, every day.

Business Companion AI gives them one calm workspace. Documents and messages are classified, summarized, extracted, and turned into suggested next actions. A human always reviews and approves before anything happens.

**Core principle:** AI prepares. Humans approve.

**Target customer:** Romanian SMEs with 5–50 employees that handle many recurring documents but do not have an internal automation or AI team. Best early fits: accounting offices, small service companies, construction companies, agencies, clinics.

---

## Modules

There are six modules in the product. Not all are built yet.

### Module 1 — AI Inbox

The central workspace. Each uploaded document or email becomes a structured card.

Each card shows:
- Document type (invoice, contract, email, HR document, etc.)
- Short summary
- Extracted fields (amounts, dates, names, CUI numbers)
- Missing information the AI could not find
- Risk flags
- Suggested next action
- Human approval status
- Full audit trail

**Status: LIVE** — see [AI Inbox](#ai-inbox-1) below

---

### Module 2 — Ask My Company

A private assistant that answers questions using only the company's own uploaded documents.

Example questions:
- "Which invoices are due this week?"
- "What did the contract with this supplier say about penalties?"
- "What documents does the accountant need from me?"

The assistant does not use outside knowledge. It only reads what the company has uploaded.

**Status: MOCK** — static demo answers today, real RAG in Slice 5

---

### Module 3 — Draft Reply Assistant

Reads incoming client, supplier, or accountant messages and prepares a reply draft.

The human reads the draft, edits it if needed, approves it, then sends it manually. The system never sends automatically.

**Status: MOCK** — static demo drafts today, real drafting in Slice 5

---

### Module 4 — Document Extraction

Pulls structured data from business documents.

Invoice fields extracted today: supplier name, CUI, invoice number, date, due date, total amount, VAT, currency, IBAN, payment status, line items, missing fields, risk flags.

Planned for Slice 4: contract extraction, document summary, document classification.

**Status: LIVE for supplier invoices** — see [Document Extraction](#document-extraction-1) below

---

### Module 5 — Human Approval & Audit Log

Every AI suggestion is marked as a suggestion. Nothing is approved or sent automatically.

Actions tracked:
- Document uploaded
- Document analyzed (by which analyzer, which prompt version)
- Human approved
- Human archived

Every AI call is logged with: prompt name, prompt version, model used, input hash, raw output, parsed output, status (success or failed).

**Status: LIVE**

---

### Module 6 — AI Literacy & Safe Use Layer

Explains to the company what the AI can and cannot do, what data it uses, and when human review is required. Planned for the onboarding package.

**Status: PLANNED — post-MVP**

---

## Current Build Status

**As of Slice 3 (2026-05-05), this is what runs:**

| What | Status | Where |
|---|---|---|
| Homepage | Live | `http://localhost:5173/` |
| Demo workflow (Atelier Nova SRL) | Live — static | `http://localhost:5173/demo` |
| AI Inbox — upload & extract | **Live — real AI** | `http://localhost:5173/app/inbox` |
| Ask My Company | Mock — static Q&A | `http://localhost:5173/app/ask` |
| Draft Reply | Mock — static drafts | `http://localhost:5173/app/inbox` (on client requests) |
| REST API | Live | `http://localhost:8000` |
| Invoice extraction | **Live — Mistral** | via API |
| Human approval | Live | via UI + API |
| Audit log | Live | via UI + API |
| Database (Postgres) | Live | port 5432 |

### AI Inbox

The inbox connects to the live backend. You can:

1. Paste any invoice text into the upload box, give it a filename and type, and submit
2. The backend sends it to the AI (Mistral) using the `invoice_extractor v1` prompt
3. Fields come back in ~5–10 seconds: supplier name, CUI, invoice number, dates, amounts, missing fields, risk flags
4. The document shows a **LIVE** badge — it is backed by real AI extraction, not mock data
5. Click Approve to record human sign-off — this creates an audit event
6. The full audit timeline (uploaded → analyzed → approved) is visible on each document

The 16 demo documents from `/demo` (Atelier Nova SRL's mock workflow) are **not shown in the inbox** — they live only in the demo page. The inbox shows only documents that have been through the real pipeline.

### Document Extraction

The extraction engine uses a pluggable Analyzer protocol. Slice 3 ships one registered analyzer:

**`invoice_extractor v1`** — handles `supplier_invoice` documents

Fields extracted:
- `supplier_name` · `supplier_cui` · `supplier_vat_number`
- `invoice_number` · `invoice_date` · `due_date`
- `total_amount` · `vat_amount` · `currency` · `iban`
- `payment_status` · `line_items[]`
- `missing_fields[]` · `risk_flags[]` · `recommended_next_action`

If the AI cannot find a field, it returns `null` — it does not invent values. Missing fields are surfaced explicitly. If the AI response is not valid JSON, the run is marked `failed` with the error message stored — no silent retries.

Every extraction is logged: prompt name, prompt version, model, SHA-256 of the input, full raw output, parsed output.

### Demo page (`/demo`)

The demo page shows a static walkthrough of the full product vision using Atelier Nova SRL — a synthetic Romanian interior design company (Pitești, 12 employees). This is the "product on a page" for pilots and sales conversations.

It contains 16 documents:
- 5 supplier invoices
- 2 client request emails
- 2 client update emails
- 2 supplier contracts
- 2 supplier offers
- 1 accountant request email
- 1 HR policy
- 1 internal procedure
- 1 price list

All data is synthetic. No real CUI, IBAN, name, or company data.

---

## Architecture

```
apps/web/          SvelteKit frontend (Svelte 5 · TypeScript · Tailwind v4)
apps/api/          FastAPI backend (Python · SQLAlchemy · Alembic)
infra/             Docker Compose (Postgres 16)
```

**Frontend → Backend:** The inbox page fetches from `http://localhost:8000/api`. The API base URL is configurable via `VITE_API_BASE_URL` in `apps/web/.env`.

**Backend → LLM:** A single adapter module (`app/services/llm.py`) wraps the OpenAI-compatible client. The provider is configured by three env vars — the same code works with Mistral, OpenAI, Ollama, or Groq.

**Analyzer pipeline:** When a document is uploaded, a background task dispatches it to all registered analyzers via `analyzers_for(doc)`. Each analyzer runs its prompt, validates the JSON output against a Pydantic schema, and writes to `DocumentAnalysis`. New analyzers in future slices are added as new files — no pipeline refactoring needed.

**Database:** 4 tables — `documents` · `document_analyses` · `audit_events` · `prompt_runs`. Every AI call has a full row in `prompt_runs` with input hash, raw output, and status.

---

## Running it locally

**Requirements:** Docker · Node.js 20+ · uv (Python)

```sh
# One command — installs missing tools, starts postgres, runs migrations
./setup.sh

# Optional: seed the 5 demo invoices
./setup.sh --seed
```

Then in two terminals:

```sh
# Terminal 1 — API
cd apps/api && uv run uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd apps/web && npm run dev
```

Open `http://localhost:5173`.

---

## Roadmap

### Slice 4 — Classifier · Summary · PDF · Evaluation harness
*Not yet started*

- Document classifier: reads any uploaded document and assigns a type automatically (no more dropdown selection required)
- Summary prompt: generates a short human-readable summary for every document type
- Contract review prompt: extracts parties, payment terms, penalties, renewal clauses, risk flags
- PDF parsing: `pdfplumber` for text-PDFs (no OCR yet)
- Evaluation harness: automated test suite that runs the prompt battery against known documents and checks extraction accuracy

After Slice 4: upload a PDF invoice, get type + summary + extracted fields automatically.

---

### Slice 5 — RAG · Ask My Company live · Draft Reply live · OCR
*Not yet seeded*

- `pgvector` embeddings for all uploaded documents
- Ask My Company becomes real: questions answered from the actual document corpus
- Draft Reply becomes real: AI drafts based on document context
- OCR for scanned documents (not born-digital)
- The product is fully functional as an end-to-end private AI operations workspace

After Slice 5: the MVP is complete. A real Romanian SME could run a pilot.

---

## What the product does NOT do (MVP boundary)

These are deliberate exclusions, not missing features:

- No automatic email sending — drafts are always reviewed by a human first
- No ANAF / SPV / e-Factura integration
- No ERP or accounting software integration
- No automatic payments
- No multi-tenant permissions or user accounts
- No mobile app
- No fine-tuning or custom model training
- No legal or accounting advice — the AI flags things for human review, it does not give professional opinions

---

## Prompt versioning

Every AI prompt used by the system is versioned. The first line of every prompt file is:

```
# prompt: <name> v<version>
```

The runner parses this line and logs the name and version in `prompt_runs`. If a prompt is changed, the version is bumped and the change is recorded. This makes it possible to trace exactly which version of a prompt produced any given extraction.

Current prompts:
- `invoice_extractor v1` — extracts invoice fields from Romanian supplier invoices

---

## Document map (where things live in the repo)

```
docs/PRD.md                     ← this file
ops/project.state.hybrid        ← live build state: current slice, patchlog
ops/rules.constraints.hybrid    ← durable product rules (do not violate)
ops/slice-N.*.hybrid            ← scope + acceptance + builder prompt per slice

apps/web/src/routes/            ← frontend pages
  +page.svelte                  ← homepage
  demo/                         ← static demo workflow
  app/inbox/                    ← live AI inbox
  app/ask/                      ← Ask My Company (mock)

apps/api/app/
  analyzers/                    ← Analyzer protocol + registry + InvoiceExtractor
  prompts/                      ← prompt template files (versioned)
  services/llm.py               ← LLM adapter (only place that calls the provider)
  services/analysis.py          ← pipeline: dispatch → run → merge → persist
  api/documents.py              ← REST endpoints
  db/models.py                  ← 4 database models

codocz/                         ← internal product definition docs (Phase 0)
  romanian_sme_ai_companion_blueprint.md
  romanian_sme_ai_companion_project_control_pack.md
  romanian_sme_ai_companion_technical_stack_decision_pack.md
  romanian_sme_ai_companion_prompt_pack.md
```
