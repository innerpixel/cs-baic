# Business Companion AI — Product Requirements Document

**Status:** Living document — updated after each build slice  
**Last updated:** 2026-05-05 · Slice 4 complete  
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
- AI-detected type and confidence badge (when the AI's classification differs from the user-selected type and confidence ≥ 60%)
- Short AI summary
- Urgency level (high · medium · low) — set by the summarizer
- Extracted fields (amounts, dates, names, CUI numbers)
- Missing information the AI could not find
- Risk flags
- Suggested next action
- Contract terms panel (collapsible — only for contract documents)
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

Pulls structured data from business documents. The extraction engine uses a pluggable Analyzer protocol. As of Slice 4, four analyzers are registered and run in this order for every applicable document:

1. **`DocumentClassifier v1`** — applies to all document types. Detects document type, confidence (0–1), language (ro/en/mixed/unknown), and named entities (companies, people, dates, amounts, emails). Does not override the user-selected type — records its finding as a soft signal.

2. **`DocumentSummarizer v1`** — applies to all document types. Produces a short summary, urgency level, key points, deadlines, amounts, obligations, and suggested next action.

3. **`InvoiceExtractor v1`** — applies to `supplier_invoice` only. Extracts: supplier name, CUI, VAT number, invoice number, dates, amounts, currency, IBAN, payment status, line items, missing fields, risk flags.

4. **`ContractReviewer v1`** — applies to `contract` only. Extracts: parties, payment terms, penalties, termination terms, renewal clause, important dates, risk flags, and flags clauses for human review.

For `supplier_invoice` documents: classifier + summarizer + invoice extractor run (3 prompt calls).  
For `contract` documents: classifier + summarizer + contract reviewer run (3 prompt calls).  
For all other types: classifier + summarizer run (2 prompt calls).

**PDF upload:** Documents can be uploaded as text or as `.pdf` files. PDF text is extracted with `pdfplumber`. Image-only PDFs (no extractable text) are flagged as `not_supported_yet` — OCR is planned for Slice 5.

**Status: LIVE** — all 4 analyzers active, all document types supported

---

### Module 5 — Human Approval & Audit Log

Every AI suggestion is marked as a suggestion. Nothing is approved or sent automatically.

Actions tracked:
- Document uploaded
- Document analyzed (by which analyzer, which prompt version)
- `ocr_required` (for image-only PDF uploads)
- Human approved

Every AI call is logged with: prompt name, prompt version, model used, input hash, raw output, parsed output, status (success or failed).

**Status: LIVE**

---

### Module 6 — AI Literacy & Safe Use Layer

Explains to the company what the AI can and cannot do, what data it uses, and when human review is required. Planned for the onboarding package.

**Status: PLANNED — post-MVP**

---

## Current Build Status

**As of Slice 4 (2026-05-05), this is what runs:**

| What | Status | Where |
|---|---|---|
| Homepage | Live | `http://localhost:5173/` |
| Demo workflow (Atelier Nova SRL) | Live — static | `http://localhost:5173/demo` |
| AI Inbox — upload, classify, summarize, extract | **Live — real AI** | `http://localhost:5173/app/inbox` |
| Ask My Company | Mock — static Q&A | `http://localhost:5173/app/ask` |
| Draft Reply | Mock — static drafts | `http://localhost:5173/app/inbox` (on client requests) |
| REST API | Live | `http://localhost:8000` |
| Document classification | **Live — all types** | via API |
| Document summarization | **Live — all types** | via API |
| Invoice extraction | **Live — supplier_invoice** | via API |
| Contract review | **Live — contract** | via API |
| PDF text upload | **Live** | via API + UI |
| Urgency badge | **Live** | inbox UI |
| Classifier disagreement badge | **Live** | inbox UI |
| Contract terms panel | **Live** | inbox UI |
| Human approval | Live | via UI + API |
| Audit log | Live | via UI + API |
| Eval harness | **Live — CLI** | `uv run python -m app.evals.run` |
| Database (Postgres) | Live | port 5432 |

---

### AI Inbox

The inbox connects to the live backend. You can:

1. Paste document text (or upload a `.pdf` file), give it a filename and type, and submit
2. The backend dispatches it to all applicable analyzers in order
3. Within 5–15 seconds (depends on number of analyzers):
   - A short AI summary appears at the top of the detail panel
   - Urgency badge (high/medium/low) appears in the header
   - A classifier badge appears if the AI detected a different type with ≥ 60% confidence
   - Extracted fields are shown (for invoices: amounts, dates, CUI, etc.)
   - Missing information and risk flags are listed
   - For contracts: a collapsible "Contract Terms" panel shows payment terms, penalties, termination terms, and any clauses the AI flagged for human review
4. Click Approve to record human sign-off — this creates an audit event

**7 demo documents** are seeded by `seed_demo.py`: 5 supplier invoices, 1 supplier contract, 1 accountant request email. All run through the full analyzer pipeline.

### Document Extraction

Each analyzer run is logged in `prompt_runs` (prompt name, version, model, input SHA-256, raw output, parsed output, status). The full parsed output for every analyzer is stored in `document_analyses.analyzer_outputs` (JSONB), keyed by analyzer name — this is the single source of truth for any detail view that needs more than the merged scalar columns.

Merged scalar columns (always the current best value across all analyzers):

| Column | Source |
|---|---|
| `summary` | DocumentSummarizer |
| `urgency` | DocumentSummarizer |
| `suggested_action` | InvoiceExtractor (wins over summarizer when present) |
| `fields` | InvoiceExtractor |
| `missing_fields` | union of InvoiceExtractor + DocumentSummarizer |
| `risk_flags` | union of InvoiceExtractor + ContractReviewer |
| `detected_type` | DocumentClassifier |
| `confidence` | DocumentClassifier |
| `language` | DocumentClassifier |
| `analyzer_outputs` | full per-analyzer output dict |

### Eval Harness

The eval harness runs the prompt battery against 4 known fixtures (from §23.3 of the project control pack) and scores each output. Results are written to `apps/api/tests/evals/results/<timestamp>.json`.

```sh
cd apps/api && uv run python -m app.evals.run
# Optional: filter by fixture or analyzer
uv run python -m app.evals.run --fixture invoice_lumina --analyzer invoice_extractor
```

**Current pass rate: 9/10.** The 1 expected failure: `invoice_extractor` misses the freeform PO-reference note on the Lumina invoice — this is a known LLM accuracy gap, caught by design, tracked for a future prompt revision.

Pass threshold: score ≥ 7, zero critical errors, zero hallucinations.

### Demo page (`/demo`)

The demo page shows a static walkthrough of the full product vision using Atelier Nova SRL — a synthetic Romanian interior design company (Pitești, 12 employees). This is the "product on a page" for pilots and sales conversations.

It contains 16 documents across all document types. All data is synthetic. No real CUI, IBAN, name, or company data.

---

## Architecture

```
apps/web/          SvelteKit frontend (Svelte 5 · TypeScript · Tailwind v4)
apps/api/          FastAPI backend (Python · SQLAlchemy · Alembic)
infra/             Docker Compose (Postgres 16)
```

**Frontend → Backend:** The inbox page fetches from `http://localhost:8000/api`. The API base URL is configurable via `VITE_API_BASE_URL` in `apps/web/.env`.

**Backend → LLM:** A single adapter module (`app/services/llm.py`) wraps the OpenAI-compatible client. The provider is configured by three env vars — the same code works with Mistral, OpenAI, Ollama, or Groq.

**Analyzer pipeline:** When a document is uploaded, a background task dispatches it to all registered analyzers via `analyzers_for(doc)`. Each analyzer runs its prompt, validates the JSON output against a Pydantic schema, and writes to `DocumentAnalysis` via `merge_into_analysis()`. New analyzers in future slices are added as new files in `app/analyzers/` and registered in `registry.py` — no pipeline refactoring needed (proven by adding 3 analyzers in Slice 4 with zero edits to `analysis.py`).

**Database:** 4 tables:
- `documents` — filename, type, status, raw_text
- `document_analyses` — merged analysis results (fields, summary, urgency, detected_type, confidence, language, analyzer_outputs JSONB, and more)
- `audit_events` — uploaded, analyzed, ocr_required, approved
- `prompt_runs` — every LLM call with prompt name/version, model, input hash, raw output, parsed output, status

---

## Running it locally

**Requirements:** Docker · Node.js 20+ · uv (Python)

```sh
# One command — installs missing tools, starts postgres, runs migrations
./setup.sh

# Seed the 7-doc demo set (5 invoices + 1 contract + 1 accountant email)
cd apps/api && uv run python scripts/seed_demo.py
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
**Complete — 2026-05-05**

- Document classifier: assigned type, confidence, language, and named entities for all document types
- Summary prompt: short summary and urgency for all document types
- Contract review: payment terms, penalties, termination, risk flags, human-review questions
- PDF parsing: `pdfplumber` for text-PDFs (image-only PDFs flagged as `not_supported_yet`)
- Evaluation harness: 4 fixtures × applicable analyzers, 9/10 pass, 1 known gap tracked
- Frontend: urgency badge, classifier disagreement badge, collapsible contract terms panel
- Seed: 7-doc demo set

---

### Slice 5 — RAG · Ask My Company live · Draft Reply live · OCR
*Not yet seeded*

- `pgvector` embeddings for all uploaded documents
- Ask My Company becomes real: questions answered from the actual document corpus
- Draft Reply becomes real: AI drafts based on document context
- OCR for scanned documents (image-only PDFs that fail today)
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
- No legal or accounting advice — the AI flags clauses for human review, it does not give professional opinions
- No OCR (image-only PDFs) — planned for Slice 5

---

## Prompt versioning

Every AI prompt used by the system is versioned. The first line of every prompt file is:

```
# prompt: <name> v<version>
```

The runner parses this line and logs the name and version in `prompt_runs`. If a prompt is changed, the version is bumped and the change is recorded. This makes it possible to trace exactly which version of a prompt produced any given extraction.

Current prompts:

| Prompt | Applies to | What it produces |
|---|---|---|
| `invoice_extractor v1` | `supplier_invoice` | supplier name, CUI, amounts, dates, line items, missing fields |
| `classifier v1` | all types | document_type, confidence, language, detected entities |
| `summarizer v1` | all types | short_summary, urgency, key_points, deadlines, amounts, obligations |
| `contract_reviewer v1` | `contract` | payment terms, penalties, termination, risk flags, human-review questions |

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

apps/web/src/lib/
  api/client.ts                 ← API client + TypeScript types
  components/ClassifierBadge.svelte    ← classifier disagreement badge
  components/ContractTermsPanel.svelte ← collapsible contract terms

apps/api/app/
  analyzers/                    ← Analyzer protocol + registry
    base.py                     ← AnalyzerResult + Analyzer Protocol
    registry.py                 ← ANALYZERS list + analyzers_for()
    classifier.py               ← DocumentClassifier
    summarizer.py               ← DocumentSummarizer
    invoice_extractor.py        ← InvoiceExtractor
    contract_reviewer.py        ← ContractReviewer
    merge.py                    ← merge_into_analysis() (isinstance dispatch)
  prompts/                      ← versioned prompt template files (.txt)
  schemas/                      ← Pydantic output models
    extraction.py               ← InvoiceExtraction
    classification.py           ← Classification
    summary.py                  ← Summary
    contract.py                 ← ContractReview
    documents.py                ← API response schemas
  services/
    llm.py                      ← LLM adapter (only place that calls the provider)
    analysis.py                 ← pipeline: dispatch → run → merge → persist
    prompts.py                  ← load_prompt() + substitute()
    parsing.py                  ← parse_pdf() via pdfplumber
  api/documents.py              ← REST endpoints (text or PDF upload)
  evals/                        ← eval harness
    fixtures.py                 ← 4 test fixtures with expected outputs
    scoring.py                  ← EvalScore model (score 0-10, errors, hallucinations)
    runner.py                   ← evaluate() + run_all()
    run.py                      ← CLI entry point
  db/models.py                  ← 4 database models

apps/api/alembic/versions/      ← database migrations
  0001_initial_schema.py
  0002_slice4_analysis_columns.py   ← 5 new columns (detected_type, confidence, language, urgency, analyzer_outputs)

apps/api/scripts/
  seed_demo.py                  ← seeds 7-doc demo set (replaces seed_invoices.py)

apps/api/tests/
  fixtures/sample_invoice.pdf   ← text-PDF fixture for PDF parsing tests
  evals/results/                ← eval run results (local-only, gitignored)

codocz/                         ← internal product definition docs (Phase 0)
  romanian_sme_ai_companion_blueprint.md
  romanian_sme_ai_companion_project_control_pack.md
  romanian_sme_ai_companion_technical_stack_decision_pack.md
  romanian_sme_ai_companion_prompt_pack.md
```
