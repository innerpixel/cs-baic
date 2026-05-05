# Romanian SME AI Companion — Product Blueprint

## 1. Core Recommendation

Build the project in this order:

1. **Define the product as a website / product page first**
2. **Use that website as the public-facing specification**
3. **Build a small working demo around the exact flows shown on the website**
4. **Test the demo with 3–5 real Romanian SME workflows**
5. **Only then expand into a modular platform**

The website is not just branding. It becomes the product mirror:

- What problem we solve
- Who it is for
- What documents it handles
- What the AI actually does
- What the user sees
- What is automated
- What stays human-approved
- How data is protected
- What a pilot includes
- What is not promised

This creates clarity before writing too much code.

---

## 2. Product Working Name

### Recommended public name direction

**Business Companion**

Possible Romanian-market names:

- **CompanionOps**
- **NexusOps AI**
- **Birou AI Companion**
- **Companion pentru Afaceri**
- **DocuCompanion AI**
- **Companion Inbox**
- **Cubic Office AI**

For the first version, avoid names that sound too abstract or cosmic. The product can be powered by the deeper CSMCL architecture, but the Romanian SME buyer needs something direct and trustworthy.

Recommended positioning:

> **A private AI operations companion for Romanian SMEs — documents, invoices, emails, contracts, and company knowledge in one intelligent workspace.**

---

## 3. The Product Thesis

Romanian SMEs do not need “AI transformation” as a slogan.

They need help with:

- too many documents
- slow replies to clients
- invoice and accountant communication
- scattered company knowledge
- contracts and supplier emails
- compliance anxiety
- repeated administrative tasks
- lack of internal documentation
- fear of using AI incorrectly

The product should feel like:

> “A calm, private AI assistant that reads the company’s operational mess and turns it into clear next actions.”

---

## 4. First Product: AI Document & Operations Inbox

### Core concept

A company forwards or uploads business documents into one workspace.

The system classifies, summarizes, extracts, routes, and prepares next actions.

### Inputs

- PDFs
- scanned documents
- invoices
- contracts
- supplier offers
- client emails
- HR documents
- accountant requests
- public company procedures
- product sheets
- Excel/CSV files later
- ANAF/SPV/e-Factura exports later

### Outputs

- document type
- summary
- extracted fields
- urgency level
- missing information
- suggested action
- draft reply
- assigned category/person
- searchable company knowledge
- audit trail

---

## 5. Primary Modules

## Module 1 — AI Inbox

The central workspace.

Each uploaded/forwarded item becomes an AI-analyzed card.

Card fields:

- Document title
- Type: invoice, contract, email, HR, supplier offer, client request, unknown
- Short summary
- Extracted data
- Urgency
- Risk flags
- Missing information
- Suggested next action
- Status: new, reviewed, assigned, done, archived
- Human approval marker

### Example

A supplier invoice arrives.

The AI card shows:

- Type: Supplier invoice
- Supplier: Example SRL
- Amount: 3,420 RON
- Due date: 17 May 2026
- Missing: purchase order reference
- Suggested action: ask supplier for PO reference and forward invoice to accountant
- Draft email prepared

---

## Module 2 — Ask My Company

A private company knowledge assistant.

The user can ask questions over uploaded documents.

Examples:

- “Which invoices are due this week?”
- “Summarize the contract with Supplier X.”
- “What did we agree about payment terms?”
- “Which client emails are waiting for a reply?”
- “Draft a reply based on our standard policy.”
- “What documents should I send to the accountant?”

Important rule:

The assistant should answer based only on company documents unless the user explicitly enables outside knowledge.

---

## Module 3 — Email Reply Assistant

The system reads incoming client/supplier/accountant emails and prepares replies.

Human approval is required before sending.

Capabilities:

- summarize email thread
- identify requested action
- detect missing information
- draft Romanian/English replies
- keep tone professional
- prepare accountant-forwarding notes
- create task from email

---

## Module 4 — Document Extraction

Structured extraction from operational documents.

Initial extraction fields:

### Invoice

- supplier name
- CUI/VAT number
- invoice number
- date
- due date
- amount
- currency
- VAT
- IBAN
- status
- missing fields

### Contract

- parties
- start date
- end date
- renewal clause
- payment terms
- penalties
- obligations
- termination clause
- risks

### Client request

- requester
- topic
- urgency
- required reply
- missing details
- suggested next step

---

## Module 5 — Human Approval & Audit

This is essential for trust.

The AI should not silently act on important business items.

Actions should be marked as:

- AI suggested
- human reviewed
- human approved
- sent/exported
- archived

Every AI-generated answer should keep source references where possible.

This avoids the “AI black box” feeling.

---

## Module 6 — AI Literacy & Safe Use Layer

A small but powerful trust module.

It explains to the company:

- what the AI can do
- what it cannot do
- what data it uses
- where the data is stored
- how hallucinations are reduced
- when human approval is required
- what employees should not upload
- how sensitive data is handled

This can become part of the paid onboarding package.

---

## 6. Website Structure

The first website should be a product definition website, not a generic agency website.

### Page 1 — Home

Goal: explain the product in 10 seconds.

Hero message:

> **Your company documents, emails, invoices, and contracts — organized by a private AI companion.**

Sub-message:

> Built for Romanian SMEs that want less paperwork, faster replies, and safer access to company knowledge.

Primary CTA:

> Request a Pilot

Secondary CTA:

> See Example Workflow

Sections:

1. Problem
2. What it does
3. Demo workflow
4. Modules
5. Trust & privacy
6. Pilot offer
7. Contact

---

### Page 2 — Product

Explain modules in detail:

- AI Inbox
- Ask My Company
- Email Assistant
- Document Extraction
- Human Approval
- Audit Log
- Safe AI Use

Each module should have one real example.

---

### Page 3 — Demo Workflow

This is the most important page.

Show a realistic business scenario.

Scenario:

> A Romanian SME receives supplier invoices, a client request, and an accountant email. The AI Companion reads everything, classifies the items, extracts important information, prepares replies, and shows what needs human approval.

Demo steps:

1. Upload documents or forward emails
2. AI creates inbox cards
3. AI extracts key data
4. AI flags missing information
5. AI drafts reply
6. Human approves
7. Task is completed or exported

This page should include screenshots or mock UI cards.

---

### Page 4 — For Romanian SMEs

Speak directly to local pain:

- invoices
- accountant communication
- supplier documents
- client messages
- contracts
- HR files
- compliance anxiety
- small teams with too much admin

Tone:

Practical, calm, trustworthy.

Avoid:

- hype
- futuristic slogans
- too much “AI revolution” language
- vague “digital transformation” text

---

### Page 5 — Security & Privacy

This page is a differentiator.

Explain:

- EU hosting option
- optional local/private deployment later
- role-based access later
- no automatic public sharing
- human approval before sending
- audit logs
- source-grounded answers
- data deletion policy
- GDPR-aware design

Even if not all features are built yet, define the direction clearly and honestly.

Use labels:

- Available in MVP
- Planned
- Enterprise option

---

### Page 6 — Pilot

Sell a concrete pilot, not a vague project.

Recommended pilot offer:

> **14-day AI Operations Pilot**

Includes:

- one company workspace
- up to X uploaded documents
- 2–3 business workflows configured
- AI Inbox demo
- Ask My Company demo
- email reply drafting demo
- final report with automation opportunities

Pilot outcome:

- document map
- workflow map
- AI readiness score
- list of automations worth building
- demo workspace

---

## 7. MVP Scope

### MVP goal

Build a small but convincing product demo that proves the core value.

### MVP should include

1. User login or simple protected workspace
2. Document upload
3. AI document classification
4. AI summary
5. Basic extraction fields
6. Search / Ask My Company
7. Draft reply generation
8. Human approval status
9. Simple audit log
10. Demo dataset

### MVP should not include yet

- full ERP integration
- automatic sending without approval
- complex multi-tenant enterprise permissions
- native e-Factura integration
- SEAP/ANAF automation
- payment system
- full CRM
- advanced analytics
- mobile app

---

## 8. Demo Dataset

Create a fake but realistic Romanian SME dataset.

Business example:

**“Atelier Nova SRL”** — a small company selling services/products.

Documents:

- 5 supplier invoices
- 3 client emails
- 2 supplier offers
- 1 accountant request
- 2 contracts
- 1 HR policy
- 1 internal procedure
- 1 product/service price list

The demo must be safe and fully synthetic.

This lets you show the product without needing client data.

---

## 9. Technical Architecture Overview

Recommended architecture for development:

### Frontend

- Vue 3 or React
- Dashboard UI
- Upload area
- AI Inbox cards
- Ask My Company interface
- Document detail view
- Human approval controls

### Backend

- FastAPI, Rust, or Node depending on existing comfort
- API gateway
- document ingestion service
- classification/extraction service
- RAG service
- audit log service
- user/workspace service

### Storage

- PostgreSQL for structured data
- object storage or filesystem for documents
- vector database for embeddings
- Redis for queues/session/cache if useful

### AI Layer

- LLM provider abstraction
- local model support later
- prompt templates
- extraction prompts
- classification prompts
- RAG prompts
- evaluation tests
- fallback models

### Document Processing

- PDF parsing
- OCR later for scanned documents
- metadata extraction
- chunking
- embeddings
- source references

### Security

- workspace isolation
- access control
- encrypted storage later
- audit logs
- human approval
- data deletion flow

---

## 10. Development Phases

## Phase 0 — Product Definition

Output:

- product website copy
- module definitions
- demo workflow
- pilot package
- synthetic Romanian SME dataset
- architecture map

This is where we are now.

---