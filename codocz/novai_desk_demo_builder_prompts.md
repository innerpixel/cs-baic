# NovAI Desk Demo Builder Prompts

Working product context:

- Product / public direction: **NovAI Desk** 
- Core idea: **AI Operations Inbox for Romanian and European SMEs**
- Principle: **AI prepares. Humans approve.**
- Current mode: MVP dogfood / public demo refinement
- Goal: Create a public demo experience that feels useful, trustworthy, realistic, and shippable.

These prompts are intended for later IDE/build sessions. They preserve the current understanding and guide implementation without reopening the entire product strategy.

---

# Overview

We now see three connected builder tasks:

1. **Public AI Inbox Demo Experience with Atelier Nova SRL**
2. **Urban Novel Desk Synthetic Company Archive Package**
3. **Ask My Company Guided Archive Experience and Evaluation**

The split is intentional.

## Atelier Nova SRL

Purpose:

> Quick AI Inbox demo.

It should show how a small set of realistic business documents becomes structured AI Inbox cards.

Emotional result:

> “Oh, this is the kind of document chaos I recognize.”

## Urban Novel Desk

Purpose:

> Deeper synthetic company archive for Ask My Company.

It should be a realistic fictional company package with enough internal complexity to demonstrate company knowledge search, cross-document reasoning, source grounding, and operational guidance.

Emotional result:

> “This feels like a real company archive. I can ask useful questions and verify the answers.”

## Ask My Company

Purpose:

> Guided archive experience.

It should not feel like an empty chatbot. It should feel like querying a known company archive with visible files, source links, suggested questions, and grounded answers.

Emotional result:

> “The AI is not guessing. It is reading the archive, and I can check the sources.”

---

# Shared Source Types

Before the three tasks, introduce or preserve a simple source classification model.

Suggested values:

```json
{
  "source_type": "dev_source | demo_source | archive_source | uploaded_sample",
  "visibility": "internal | public_demo | user_session",
  "public_demo": true,
  "purpose": "classifier testing | inbox demo | archive demo | user trial"
}
```

## Source Type Meanings

### dev_source

Internal test data.

Used for:

- classifier testing
- extraction testing
- prompt regression
- RAG debugging
- edge cases

Usually not polished or public-facing.

### demo_source

Polished public demo files.

Used for:

- homepage examples
- AI Inbox demo
- source-to-AI-result demonstration
- public visitor trust

Should be visually realistic and source-viewable.

### archive_source

Files belonging to the larger Urban Novel Desk archive.

Used for:

- Ask My Company demo
- downloadable ZIP
- cross-document questions
- source-grounded answers

Should be realistic, coherent, and richly connected.

### uploaded_sample

Temporary user-uploaded sample files.

Used for:

- visitor trial
- one PDF or small ZIP later
- temporary mini workspace
- no automatic sending

Should be handled with clear privacy and safety messaging.

---

# Prompt 1: Public AI Inbox Demo Experience with Atelier Nova SRL

## Use this prompt in the IDE/build assistant

```text
We need to improve the public AI Inbox demo experience for NovAI Desk / Business Companion AI.

Current product context:
The app already has a SvelteKit frontend, FastAPI backend, PostgreSQL with pgvector, AI Inbox, document classification, summarization, invoice extraction, contract review, RAG Ask My Company, draft replies, Romanian business language support, and synthetic development data.

The current demo/test data was created mainly for development. Some source material may currently live as TypeScript seed data rather than realistic files. That was useful for building classifiers and testing flows, but the public visitor experience now needs to become more realistic and emotionally understandable.

Goal:
Create a visitor-facing AI Inbox demo using Atelier Nova SRL as the quick demo company.

The visitor should be able to:
1. See realistic sample business documents.
2. Inspect the original source file.
3. See what the AI Inbox extracted and suggested.
4. Understand the workflow immediately.
5. Download or re-upload sample files for play/testing.
6. Feel: “This is the kind of business document problem I have.”

Core experience:
Original source document → AI Inbox card → extracted fields → missing information → suggested action → human review.

Important:
Do not build a full SaaS account system.
Do not integrate Gmail or Microsoft yet.
Do not redesign the whole architecture.
Focus on making the public AI Inbox demo visible, realistic, and trustworthy.

Required work:

1. Clean up current dev/test data classification.
   - Existing test/demo seed data should be marked as dev_source if it is mainly internal/testing-oriented.
   - Preserve current data for regression testing.
   - Do not delete useful test data.
   - Add metadata where practical:
     source_type: dev_source
     visibility: internal
     public_demo: false
     purpose: classifier/extraction/RAG testing

2. Create polished Atelier Nova SRL public demo documents.
   - Create realistic synthetic files for public demo use.
   - These should be marked:
     source_type: demo_source
     visibility: public_demo
     public_demo: true
     company: Atelier Nova SRL

3. Use approximately 3 files per major classifier category over time.
   Initial categories:
   - supplier_invoice
   - client_request
   - accountant_request
   - contract
   - supplier_offer
   - internal_procedure or price_list

   Not every file needs to be shown on the homepage. The public demo can show a curated subset first.

4. Make demo documents realistic.
   Each public demo source should be a file the visitor can understand.
   Prefer browser-viewable PDFs where appropriate.
   Use:
   - fake logo
   - fake but plausible company identity
   - fake CUI
   - fake IBAN
   - fake email addresses
   - Romanian business language
   - realistic formatting
   - dates
   - amounts
   - payment terms
   - missing information where useful

   All data must be synthetic.

5. Add source visibility from AI Inbox cards.
   Each AI Inbox card should clearly show:
   - source filename
   - document type
   - status
   - urgency
   - extracted highlights
   - missing information
   - suggested action
   - human review status

   Add actions:
   - View source
   - Ask about this
   - Draft reply
   - Mark needs review
   - Mark approved or done if already supported

6. Implement or improve View source.
   From a card, the visitor should be able to open the source document.
   The source view should show:
   - PDF preview if available
   - raw extracted text in a separate section or tab
   - metadata
   - AI analysis connected to the source
   - processing status

   This is important for trust. The visitor must see the relationship between the original file and the AI result.

7. Add homepage demo hook.
   On the homepage or public demo page, show a simple side-by-side:
   Left:
   - original document preview
   Right:
   - AI Inbox result card

   Suggested section title:
   “See what the AI Inbox does”

   Suggested copy:
   “Start with a real-looking business document. The AI Inbox classifies it, extracts key fields, finds missing information, and prepares the next action for human review.”

   CTAs:
   - Explore demo inbox
   - Try a sample document

8. Allow safe sample play.
   If upload already exists, expose a clear public pathway:
   - user can upload one PDF
   - later support ZIP with up to 10 PDFs
   - the system creates a temporary mini result
   - show AI Inbox card after processing

   Public safety copy:
   “For this public demo, please use anonymized or non-sensitive files. AI results are suggestions and should be reviewed by a human.”

9. Allow user to download sample files.
   The visitor should be able to download one or more Atelier Nova sample files.
   They can inspect them locally and optionally upload them back to test classification.

10. Keep the frontend focused on experience.
   The demo should produce the reaction:
   “Oh, this is my kind of problem. Let me try one.”

Acceptance criteria:
- Existing development seed data is clearly separated or marked as dev_source.
- Atelier Nova SRL public demo files exist as source-viewable demo_source files.
- AI Inbox cards show source filenames and clear extracted highlights.
- Visitor can click View source from an AI Inbox card.
- Visitor can see original file and AI result in a connected way.
- Homepage or demo page includes a source-to-AI-result example.
- There is a visible “Try your own sample” or “Try a sample document” path.
- Public demo copy explains human review and safe/anonymized upload.
- No large architecture rewrite is introduced.

Final UX anchor:
Show the source. Show the AI result. Invite the user to try a sample.
```

---

# Prompt 2: Urban Novel Desk Synthetic Company Archive Package

## Use this prompt in a separate IDE/content generation session

```text
We need to create a realistic synthetic company archive package for the Ask My Company demo experience of NovAI Desk / Business Companion AI.

This task is about creating the fake company world and document package. It is not primarily a UI task and not primarily a backend task.

Working package name:
Urban Novel Desk

Purpose:
Urban Novel Desk is a fictional but realistic Romanian SME archive used to demonstrate Ask My Company. The user can inspect, download, and ask AI questions about the same documents.

The word “Novel” intentionally signals a crafted fictional company world. It should feel playful internally, but the user-facing experience must still feel business-realistic.

Goal:
Create a downloadable, ingestible synthetic company archive with realistic files, document tree, metadata, guide, expected questions, and expected grounded answers.

The archive should demonstrate real complications that SMEs face:
- scattered invoices
- accountant requests
- missing documents
- unclear approvals
- contracts with payment terms and penalties
- supplier offers with expiration dates
- client requests missing information
- project documents spread across multiple folders
- internal procedures needed to answer client emails
- cross-document relationships
- recurring monthly reporting pressure

The package should feel like:
“This is a real enough company archive that I can imagine my own company inside it.”

Company concept:
Urban Novel Desk is a synthetic Romanian SME that provides office planning, workspace design, custom office furniture coordination, and small renovation/project management for business clients.

It is broad enough to generate:
- client projects
- supplier contracts
- supplier invoices
- accountant communication
- price lists
- internal procedures
- HR/admin docs
- delivery issues
- software subscriptions
- project folders

Required archive structure:

urban-novel-desk-demo-package/
  README.md
  README.pdf optional
  company-profile.md
  document-tree.md
  index.json
  expected-questions.md
  expected-answers.json

  01-company/
    company-profile.pdf
    contact-details.pdf
    internal-roles.pdf

  02-accounting/
    accountant-request-april.pdf
    monthly-closing-checklist-april.pdf
    missing-documents-followup.pdf

  03-invoices/
    supplier-invoices/
    client-invoices/
    software-subscriptions/
    logistics-invoices/

  04-contracts/
    supplier-contracts/
    client-contracts/
    service-agreements/

  05-clients/
    client-requests/
    project-emails/
    complaints-or-delays/

  06-suppliers/
    supplier-offers/
    delivery-updates/
    price-negotiations/

  07-projects/
    showroom-pitesti/
    office-bucharest/
    clinic-reception-cluj/

  08-internal-procedures/
    project-intake-procedure.pdf
    client-reply-guidelines.pdf
    invoice-approval-procedure.pdf

  09-price-lists/
    services-price-list-2026.pdf
    furniture-coordination-price-list.pdf

  10-hr-admin/
    remote-work-policy.pdf
    expense-policy.pdf

Document volume:
Create enough documents to make Ask My Company meaningful. A good target:

- 10 invoices
- 10 client or supplier emails
- 6 contracts
- 5 supplier offers
- 5 internal procedures or policies
- 3 price lists
- 3 project folders with related files
- 3 accountant-related documents

The exact number can be adjusted, but the archive should contain enough cross-document relationships to support useful questions.

Document design:
Where possible, create PDF-ready content with realistic formatting. Actual PDF generation can be done later, but content should be structured so it can become PDF.

Each document should include:
- filename
- document type
- folder path
- source_type: archive_source
- visibility: public_demo
- purpose: ask_my_company_demo
- realistic text content
- key fields
- related documents
- expected classification
- expected summary
- expected extraction fields where relevant
- expected tags
- suggested questions it helps answer

All names, CUIs, IBANs, addresses, emails, and personal names must be synthetic.

Use safe fake values:
- CUI: RO000000XX
- IBAN: RO00DEMO00000000000000XX
- email domains: example.test or clearly fake demo domains
- no real company data

Important complications to include:
1. One invoice missing purchase order reference.
2. One software subscription invoice with unclear internal approver.
3. One accountant email requesting several missing documents.
4. One supplier contract with 14-day payment terms and late penalties.
5. One client contract with milestone payment terms.
6. One supplier offer expiring soon.
7. One client request missing floor plan or technical details.
8. One delayed delivery email affecting a project deadline.
9. One price list that helps draft a client reply.
10. One internal procedure explaining how to approve invoices.
11. One project folder where documents are scattered across invoice, contract, and emails.
12. One duplicate-looking invoice or confusing similar invoice number.
13. One contract renewal date that should be found by Ask My Company.
14. One HR/admin policy that should not be confused with accounting documents.
15. One document that should produce a “not found” answer for unrelated questions.

Core demo projects:
Use three named synthetic projects:

1. Showroom Pitești
   - client contract
   - supplier invoice
   - accountant request reference
   - delivery delay
   - internal project note

2. Office București
   - client request
   - price list reference
   - supplier offer
   - draft reply opportunity

3. Clinic Reception Cluj
   - service agreement
   - furniture supplier offer
   - delivery/payment terms
   - missing approval issue

README / user guide:
Create a user-facing README that explains:
- This is a synthetic company archive.
- It contains fake business documents for demo purposes.
- Users can download it, inspect it, and ask AI questions about it.
- The AI answers should cite source files.
- The experience demonstrates how Ask My Company works with a real company archive.
- No real company or personal data is included.

Suggested README text:
“Urban Novel Desk is a synthetic Romanian SME archive created to demonstrate Ask My Company. The files include invoices, contracts, accountant messages, supplier offers, project notes, price lists, and internal procedures. You can inspect the files yourself, then ask the AI questions about the same archive.”

Expected questions:
Create at least 25 suggested questions, grouped by category.

Examples:
- What documents are missing for April closing?
- Which invoices are urgent this week?
- Which invoices have missing information?
- What did the accountant request?
- Which contracts mention penalties?
- What are the payment terms with Lumina Design?
- Which documents are related to Showroom Pitești?
- Which clients need a reply?
- Which supplier offers expire soon?
- What should we ask the Office București client before sending an offer?
- Create a checklist for the accountant.
- Summarize everything related to Clinic Reception Cluj.
- Which documents mention unclear approval?
- Which invoice is related to the software subscription?
- Which documents should be reviewed by a human before action?

Expected answers:
For a subset of at least 15 questions, create expected grounded answers with source filenames.
These can later be used for evaluation.

Output requested:
1. Archive structure.
2. Full document list.
3. Metadata schema.
4. Realistic content for each document.
5. README/user guide.
6. Suggested questions.
7. Expected answers for evaluation.
8. Notes on cross-document relationships.
9. Notes on which files are best for AI Inbox re-upload play.
10. Any recommended ZIP packaging script or structure.

Do not:
- use real company data
- create misleading real-looking government/legal documents
- overcomplicate the archive with enterprise-scale details
- make everything too clean
- make Ask My Company dependent on external knowledge

Final archive anchor:
A user should be able to download the package, inspect the files, ask the AI about them, verify the sources, and understand how their own company archive could work.
```

---

# Prompt 3: Ask My Company Guided Archive Experience and Evaluation

## Use this prompt after Urban Novel Desk exists

```text
We need to refactor and polish the Ask My Company experience for NovAI Desk / Business Companion AI using the Urban Novel Desk synthetic company archive.

Current product context:
The app already has RAG / Ask My Company functionality, document ingestion, pgvector, source-grounded answers, draft replies, and honest “not found” behavior. The next step is to make Ask My Company feel like a guided company archive experience, not an empty chatbot.

Goal:
When a visitor opens Ask My Company, they should understand that they are exploring the Urban Novel Desk demo archive. They should be able to inspect or download the same files, ask useful questions, see grounded answers with sources, and trust that the AI is not guessing.

Core experience:
Known archive → guided suggested questions → grounded answer → source links → user verifies → CTA to try own company.

Important:
Do not integrate Gmail or Microsoft.
Do not build full SaaS accounts.
Do not make Ask answer from the open internet.
Do not let the AI invent information not in the archive.
Focus on guidance, source visibility, evaluation, and trust.

Required work:

1. Add an Ask My Company guide panel.
   The page should not start with only an empty input.

   It should explain:
   “You are exploring the Urban Novel Desk demo archive. This synthetic company package contains invoices, contracts, accountant messages, supplier offers, project files, price lists, and internal procedures. Ask questions as if you were a manager trying to understand what needs attention.”

   Include clear trust text:
   “Answers are generated from the indexed demo documents. Source files are shown so you can verify the answer.”

2. Add suggested questions.
   Group them by category.

   Suggested groups:
   - Accounting
   - Invoices
   - Contracts
   - Clients
   - Suppliers
   - Projects
   - Internal procedures

   Example questions:
   - What documents are missing for April closing?
   - Which invoices are urgent this week?
   - Which invoices have missing information?
   - What did the accountant request?
   - Which contracts mention penalties?
   - Which documents are related to Showroom Pitești?
   - Which clients need a reply?
   - Which supplier offers expire soon?
   - Create a checklist for the accountant.
   - Summarize everything related to Clinic Reception Cluj.

3. Show archive status.
   The Ask page should show:
   - archive name: Urban Novel Desk
   - number of documents indexed
   - number of chunks indexed if available
   - last indexed timestamp if available
   - link to download the archive ZIP if available
   - link to browse source files if available

   Example:
   “Urban Novel Desk demo archive · 42 documents indexed · 186 chunks available”

4. Improve source display.
   Every answer should show source filenames.
   Source filenames should be clickable.
   Clicking a source should open:
   - document detail
   - PDF preview if available
   - extracted raw text
   - metadata
   - AI analysis if available

   The user must be able to verify the answer.

5. Improve answer format.
   Answers should be structured for business use.

   Suggested format:
   - Direct answer
   - Key points
   - Source documents
   - Missing information if any
   - Recommended next action
   - Human review note if needed

   The UI can render the JSON or normalized answer cleanly.

6. Preserve honest not-found behavior.
   If the archive does not contain the answer, the AI should say:
   “I could not find this in the Urban Novel Desk archive.”

   It should not guess.

7. Add “Ask about this document” from AI Inbox or document detail.
   From a source document, user can ask:
   - Summarize this file
   - What action is needed?
   - What is missing?
   - Which other files mention this project or supplier?

   This can route to Ask My Company with document context.

8. Add evaluation tests against Urban Novel Desk.
   Use expected questions and expected answers from the archive package.

   Tests should check:
   - answer is grounded
   - correct source files are cited
   - no hallucinated amounts or deadlines
   - not-found behavior works
   - Romanian/English handling works if applicable
   - output structure is valid
   - human review flags appear for legal/accounting-sensitive answers

9. Create regression test set.
   Use at least:
   - 10 straightforward questions
   - 5 cross-document questions
   - 5 not-found or uncertainty questions
   - 5 action-oriented questions
   - 5 source verification questions

10. Add a CTA after successful answer exploration.
   Suggested CTA:
   “Want to ask these questions about your own company documents?”
   Buttons:
   - Try one sample document
   - Request a workflow review
   - Download demo archive

Acceptance criteria:
- Ask My Company page has a clear Urban Novel Desk guide.
- Suggested questions are visible and useful.
- Archive indexing status is visible.
- Answers cite clickable source filenames.
- Source documents can be inspected.
- At least 25 suggested questions exist.
- Evaluation tests run against a subset of expected Q&A.
- Not-found behavior is preserved.
- The page feels like exploring a company archive, not chatting with a generic bot.

Final UX anchor:
Do not make the user ask from emptiness. Give them a living archive, useful questions, grounded answers, and visible sources.
```

---

# Suggested Build Order

```text
1. Prompt 1
   Public AI Inbox Demo Experience with Atelier Nova SRL

2. Prompt 2
   Urban Novel Desk Synthetic Company Archive Package

3. Prompt 3
   Ask My Company Guided Archive Experience and Evaluation
```

## Why this order

The public AI Inbox demo gives the first visitor “wow.”

The Urban Novel Desk package gives Ask My Company real substance.

The Ask My Company refactor then uses that package as a trustworthy archive.

---

# Visitor Experience After These Tasks

The public demo should feel like this:

```text
Homepage
→ See source-to-AI-result example

AI Inbox demo
→ Explore Atelier Nova SRL processed documents

View source
→ Open original demo PDF or raw extracted text

Download sample
→ Inspect or re-upload a safe synthetic file

Ask My Company
→ Explore Urban Novel Desk archive

Download archive
→ Inspect the same files locally

Suggested questions
→ Ask useful questions with grounded answers

Try own sample
→ Upload one PDF or small ZIP later

CTA
→ Request a workflow review or pilot
```

---

# Final Product Anchor

> **Show the source. Show the AI result. Let the user ask the archive. Then invite them to try their own workflow.**

This is the public demo experience that can make a Romanian SME say:

> “Ok. I understand. Let’s talk.”
