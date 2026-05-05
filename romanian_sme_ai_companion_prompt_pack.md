# 19. Prompt Pack — From Product Definition to Build

This prompt pack is designed to guide the project from concept to website, clickable demo, AI prototype, and pilot readiness.

Use the prompts sequentially. Each prompt should produce an artifact that becomes input for the next prompt.

The process:

1. Product identity
2. Target customer
3. Product offer
4. Website structure
5. Website copy
6. Demo scenario
7. Synthetic dataset
8. Dashboard UX
9. Technical architecture
10. MVP backlog
11. AI workflow prompts
12. Testing and evaluation
13. Pilot package
14. Outreach and discovery

---

## 19.1 Master Project Orchestrator Prompt

Use this at the beginning of a planning session.

```text
You are my product strategy, architecture, and implementation partner.

We are building an AI product for Romanian SMEs.

The product is a private AI operations companion that helps companies manage documents, invoices, contracts, emails, accountant communication, and internal company knowledge.

The first version should not be a generic chatbot. It should be a practical AI Document & Operations Inbox with an Ask My Company knowledge assistant.

Our goals are:
1. Define the product clearly.
2. Create a product-definition website.
3. Build a clickable dashboard demo using synthetic Romanian SME data.
4. Implement one real AI workflow.
5. Prepare a small pilot offer for Romanian SMEs.

Important principles:
- Show concrete workflows, not vague AI claims.
- AI prepares, humans approve.
- The product must feel trustworthy, practical, Romanian-aware, and GDPR-conscious.
- Start with boring but valuable business pain.
- Avoid overbuilding before market feedback.

Your task is to help me move step by step.
For each step, produce clear output that can be used directly in development, website copy, product documentation, or implementation planning.

Start by helping me define the product identity, positioning, and first market wedge.
```

---

## 19.2 Product Identity Prompt

Use this to choose the product name, tone, and positioning.

```text
Help me define the product identity for a Romanian SME AI operations companion.

Context:
The product helps small and medium Romanian companies manage documents, invoices, contracts, emails, accountant communication, and company knowledge using AI.

The product should feel:
- practical
- trustworthy
- calm
- technically serious
- Romanian-aware
- not hype-driven
- not like a generic AI agency

Avoid language like:
- digital transformation
- next-generation AI
- revolutionary AI solution
- empower your business
- AI-powered innovation

Generate:
1. 10 possible product names.
2. 5 positioning statements.
3. 5 one-line homepage hero messages.
4. 5 short taglines.
5. Recommended tone of voice.
6. Words to use.
7. Words to avoid.
8. The strongest name + positioning combination and why.
```

---

## 19.3 Target Customer Prompt

Use this to define who the first product is for.

```text
Define the ideal first customer profile for our Romanian SME AI operations companion.

The product helps with:
- document overload
- invoices
- contracts
- supplier emails
- client requests
- accountant communication
- company knowledge search
- draft replies
- human-approved AI actions

Generate:
1. The best first customer segments in Romania.
2. The top 5 segments to avoid at the beginning.
3. The strongest beachhead segment.
4. The daily pain points of that segment.
5. The buying triggers.
6. The objections they will have.
7. How to answer each objection.
8. What demo would convince them.
9. What data/documents they would be willing to test with.
10. What a realistic pilot should include.

Be practical. Focus on customers who could realistically buy or test this within 30–60 days.
```

---

## 19.4 Product Offer Prompt

Use this to define the first commercial offer.

```text
Design the first commercial offer for our Romanian SME AI operations companion.

We do not want to sell a huge platform immediately.
We want a clear pilot package that reduces risk and creates trust.

Product concept:
A private AI Document & Operations Inbox with an Ask My Company assistant.

Generate:
1. A 14-day pilot offer.
2. A 30-day pilot offer.
3. What is included.
4. What is excluded.
5. What the customer must provide.
6. What we deliver at the end.
7. Possible pricing ranges.
8. Success metrics.
9. A simple contract/scope outline.
10. A short sales description for the website.

Make it specific enough that a Romanian SME owner understands exactly what they get.
```

---

## 19.5 Website Structure Prompt

Use this before writing the actual website.

```text
Create the full website structure for our Romanian SME AI operations companion.

The website is not just marketing. It is the product definition layer.

Pages needed:
- Home
- Product
- Demo Workflow
- For Romanian SMEs
- Security & Privacy
- Pilot
- Contact

For each page, generate:
1. Page goal.
2. Target visitor mindset.
3. Main message.
4. Section structure.
5. CTA.
6. Example content ideas.
7. What proof/demo element should appear.
8. What not to say.

The site should feel practical, serious, clear, and trustworthy.
Avoid generic AI startup language.
```

---

## 19.6 Website Copy Prompt — Homepage

Use this to generate the homepage copy.

```text
Write the homepage copy for our Romanian SME AI operations companion.

Product:
A private AI Document & Operations Inbox for Romanian SMEs.
It helps organize documents, invoices, emails, contracts, accountant communication, and company knowledge.

Tone:
- direct
- calm
- practical
- trustworthy
- no hype
- Romanian SME friendly

Homepage sections:
1. Hero
2. Problem
3. What the product does
4. Example workflow
5. Product modules
6. Human approval and trust
7. Pilot offer
8. Final CTA

Requirements:
- Avoid generic AI language.
- Use concrete examples.
- Mention that AI prepares and humans approve.
- Make the product feel real even before a full backend exists.
- Use short paragraphs.
- Include CTA button text.

Produce full copy ready to paste into a website.
```

---

## 19.7 Website Copy Prompt — Product Page

```text
Write the Product page copy for our Romanian SME AI operations companion.

Core modules:
1. AI Inbox
2. Ask My Company
3. Email Reply Assistant
4. Document Extraction
5. Human Approval & Audit Log
6. Safe AI Use Layer

For each module, include:
- what it does
- example input
- example output
- business value
- trust/safety note

Tone:
Practical, clear, Romanian SME focused, no hype.

End the page with a CTA for a pilot.
```

---

## 19.8 Demo Workflow Prompt

Use this to create the most important page and demo script.

```text
Design a realistic demo workflow for our Romanian SME AI operations companion.

The demo should show how a small Romanian company goes from messy documents to clear next actions.

Use a fake company called Atelier Nova SRL.

The demo should include:
- supplier invoice
- client request email
- accountant email
- small contract
- supplier offer
- internal procedure

Generate:
1. Demo story.
2. Step-by-step user flow.
3. Screens shown at each step.
4. AI output shown at each step.
5. What the human approves.
6. What value is obvious to the buyer.
7. Text for the Demo Workflow website page.
8. A short 3-minute live demo script.

The demo must be concrete and believable.
```

---

## 19.9 Synthetic Dataset Prompt

Use this to create safe fake demo documents.

```text
Create a synthetic Romanian SME demo dataset for our AI Document & Operations Inbox.

Company name: Atelier Nova SRL
Business type: small Romanian service/product company
Purpose: demo only, no real personal data

Create realistic sample content for:
1. 5 supplier invoices
2. 3 client emails
3. 2 supplier offers
4. 1 accountant request
5. 2 short contracts
6. 1 HR/internal policy
7. 1 internal procedure
8. 1 service price list

For each document, provide:
- filename
- document type
- realistic text content
- key fields expected to be extracted
- expected AI summary
- expected urgency
- expected suggested action

Make the documents realistic enough for testing classification, extraction, summarization, and RAG.
Keep all names, CUI numbers, IBANs, emails, and addresses synthetic.
```

---

## 19.10 Dashboard UX Prompt

Use this before building the UI.

```text
Design the dashboard UX for our Romanian SME AI operations companion.

Core screens:
1. Workspace home
2. AI Inbox
3. Document detail panel
4. Ask My Company assistant
5. Draft reply panel
6. Audit log
7. Settings / data privacy

Use synthetic data from Atelier Nova SRL.

Generate:
1. Information architecture.
2. Main navigation.
3. Components per screen.
4. Card layouts.
5. Empty states.
6. Loading states.
7. Error states.
8. Human approval interactions.
9. Trust indicators.
10. Copy/microcopy for important buttons and labels.

Design principle:
The user should understand the product in under 3 minutes.
```

---

## 19.11 Frontend Implementation Prompt

Use this inside the IDE assistant when creating the first mock frontend.

```text
Build a frontend mock dashboard for an AI Document & Operations Inbox.

Use static synthetic JSON data. Do not connect a backend yet.

Product context:
Romanian SME AI operations companion for documents, invoices, emails, contracts, accountant communication, and company knowledge.

Required screens/components:
- Layout with sidebar
- AI Inbox list
- Document cards
- Filter by document type/status/urgency
- Document detail panel
- Extracted fields section
- Suggested action section
- Draft reply panel
- Ask My Company chat mock
- Audit timeline
- Human approval button states

Use clean, professional styling.
The product should feel trustworthy, practical, and not overdesigned.

Create well-structured components and keep the mock data separated from UI logic.
Use realistic Romanian SME sample data.
```

---

## 19.12 Technical Architecture Prompt

Use this before backend development.

```text
Design the technical architecture for our Romanian SME AI operations companion.

Product modules:
- AI Inbox
- document upload
- document parsing
- document classification
- field extraction
- summarization
- Ask My Company RAG assistant
- draft reply generation
- human approval
- audit log
- workspace/user management

Constraints:
- Start simple.
- Build an MVP first.
- Make it modular enough to expand later.
- Prefer EU/GDPR-aware data handling.
- Avoid overengineering.
- Support local/private deployment later if needed.

Generate:
1. High-level architecture.
2. Service/module boundaries.
3. Suggested database schema.
4. API endpoints.
5. Document ingestion pipeline.
6. Vector search/RAG pipeline.
7. AI provider abstraction.
8. Queue/background job needs.
9. Audit logging model.
10. Security considerations.
11. MVP version vs later version.
12. Recommended development order.
```

---

## 19.13 Backend MVP Prompt

Use this inside the IDE assistant for backend planning/implementation.

```text
Help me build the backend MVP for an AI Document & Operations Inbox.

MVP features:
1. Create workspace.
2. Upload document.
3. Store document metadata.
4. Parse text from document.
5. Classify document type.
6. Summarize document.
7. Extract basic fields for invoices and emails.
8. Store AI analysis result.
9. Expose inbox API.
10. Expose document detail API.
11. Create audit log entries.

Keep the first version simple and testable.

Generate:
- folder structure
- database schema
- API route list
- processing flow
- background job design if needed
- error handling strategy
- test plan

Do not add unnecessary enterprise features yet.
```

---

## 19.14 AI Classification Prompt

This is a runtime prompt template for classifying uploaded documents.

```text
You are an AI document classifier for a Romanian SME operations inbox.

Classify the document into exactly one of these types:
- supplier_invoice
- client_invoice
- contract
- supplier_offer
- client_request
- accountant_request
- hr_document
- internal_procedure
- price_list
- unknown

Return only valid JSON with this schema:

{
  "document_type": "one_of_the_allowed_types",
  "confidence": 0.0,
  "reason": "short explanation",
  "language": "ro|en|mixed|unknown",
  "detected_entities": {
    "company_names": [],
    "people_names": [],
    "dates": [],
    "amounts": [],
    "emails": []
  }
}

Document text:
---
{{DOCUMENT_TEXT}}
---
```

---

## 19.15 AI Summary Prompt

Runtime prompt template.

```text
You are an AI operations assistant for a Romanian SME.

Summarize the document for a busy business owner.

Requirements:
- Be concise.
- Mention what the document is about.
- Mention any deadlines, amounts, obligations, or requested actions.
- Mention missing information if obvious.
- Do not invent details.
- If information is unclear, say so.

Return valid JSON:

{
  "short_summary": "1-2 sentence summary",
  "key_points": [],
  "deadlines": [],
  "amounts": [],
  "obligations": [],
  "missing_information": [],
  "recommended_next_action": "clear practical action",
  "urgency": "low|medium|high|unknown"
}

Document text:
---
{{DOCUMENT_TEXT}}
---
```

---

## 19.16 Invoice Extraction Prompt

Runtime prompt template.

```text
You are an AI extraction engine for Romanian business invoices.

Extract invoice information from the document.

Rules:
- Return only valid JSON.
- Do not invent missing fields.
- Use null when a field is not found.
- Preserve original currency and date format if uncertain.
- Flag suspicious or missing data.

Schema:

{
  "supplier_name": null,
  "supplier_cui": null,
  "supplier_vat_number": null,
  "invoice_number": null,
  "invoice_date": null,
  "due_date": null,
  "total_amount": null,
  "vat_amount": null,
  "currency": null,
  "iban": null,
  "payment_status": "unknown",
  "line_items": [
    {
      "description": null,
      "quantity": null,
      "unit_price": null,
      "amount": null
    }
  ],
  "missing_fields": [],
  "risk_flags": [],
  "recommended_next_action": null
}

Invoice text:
---
{{DOCUMENT_TEXT}}
---
```

---

## 19.17 Contract Review Prompt

Runtime prompt template.

```text
You are an AI assistant helping a Romanian SME understand a business contract.

You are not a lawyer and you must not provide legal advice.
Your task is to summarize operationally relevant information and flag clauses that need human/legal review.

Return valid JSON:

{
  "contract_type": null,
  "parties": [],
  "start_date": null,
  "end_date": null,
  "payment_terms": [],
  "obligations": [],
  "termination_terms": [],
  "penalties": [],
  "renewal_clause": null,
  "important_dates": [],
  "risk_flags": [],
  "questions_for_human_review": [],
  "plain_language_summary": "short summary",
  "recommended_next_action": "practical next step"
}

Contract text:
---
{{DOCUMENT_TEXT}}
---
```

---

## 19.18 Email Reply Draft Prompt

Runtime prompt template.

```text
You are an AI assistant drafting a business email reply for a Romanian SME.

Context:
The AI prepares drafts, but a human must review and approve before sending.

Write a professional reply based only on the provided email/thread and company context.

Rules:
- Do not invent commitments.
- If information is missing, ask for clarification.
- Keep the tone polite, clear, and practical.
- Use Romanian unless the original email is in English.
- Do not send the email. Only draft it.

Return valid JSON:

{
  "detected_language": "ro|en|mixed|unknown",
  "reply_subject": "draft subject",
  "reply_body": "draft email body",
  "assumptions": [],
  "missing_information": [],
  "human_review_required": true,
  "recommended_next_action": "what the human should check before sending"
}

Incoming email/thread:
---
{{EMAIL_TEXT}}
---

Relevant company context:
---
{{COMPANY_CONTEXT}}
---
```

---

## 19.19 Ask My Company RAG Prompt

Runtime prompt template.

```text
You are a private company knowledge assistant for a Romanian SME.

Answer the user's question using only the provided company context.

Rules:
- If the answer is not in the provided context, say that the information was not found.
- Do not invent policies, dates, prices, legal obligations, or commitments.
- Cite the source document names when possible.
- Keep the answer practical and concise.
- If the question requires human/accountant/legal review, say so clearly.

Return valid JSON:

{
  "answer": "clear answer",
  "source_documents": [],
  "confidence": "low|medium|high",
  "missing_information": [],
  "recommended_next_action": null,
  "requires_human_review": false
}

User question:
---
{{USER_QUESTION}}
---

Company context:
---
{{RETRIEVED_CONTEXT}}
---
```

---

## 19.20 Human Approval Decision Prompt

Runtime prompt template for suggesting approval state.

```text
You are an AI operations assistant.

Review the proposed AI action and decide whether it is safe to present for human approval.

You must not approve the action yourself.
You only recommend whether the action is ready for human review or needs more information.

Return valid JSON:

{
  "ready_for_human_review": true,
  "blocking_issues": [],
  "items_human_should_check": [],
  "risk_level": "low|medium|high",
  "suggested_status": "ready_for_review|needs_more_information|do_not_send",
  "explanation": "short explanation"
}

Original document/email:
---
{{SOURCE_TEXT}}
---

Proposed AI action:
---
{{PROPOSED_ACTION}}
---
```

---

## 19.21 AI Evaluation Prompt

Use this to evaluate whether outputs are good enough.

```text
Evaluate the AI output for a Romanian SME operations assistant.

Check for:
1. Accuracy.
2. Whether the AI invented information.
3. Whether important dates, amounts, obligations, or risks were missed.
4. Whether the tone is appropriate.
5. Whether human review is correctly required.
6. Whether the output is useful for a business owner.
7. Whether the JSON format is valid.

Return:

{
  "score": 0-10,
  "passed": true_or_false,
  "issues": [],
  "hallucinations_detected": [],
  "missing_critical_information": [],
  "format_errors": [],
  "recommended_improvements": []
}

Original input:
---
{{INPUT_TEXT}}
---

AI output:
---
{{AI_OUTPUT}}
---
```

---

## 19.22 MVP Backlog Prompt

Use this to convert the project into build tasks.

```text
Create an MVP backlog for our Romanian SME AI operations companion.

MVP goal:
A believable product website, clickable dashboard demo, and one working AI document workflow.

Break the work into:
1. Website tasks.
2. Frontend dashboard tasks.
3. Backend tasks.
4. AI pipeline tasks.
5. Data/model tasks.
6. Security/privacy tasks.
7. Testing tasks.
8. Demo/pilot preparation tasks.

For each task include:
- task title
- user story
- acceptance criteria
- priority
- estimated complexity: small/medium/large
- dependencies

Keep the backlog practical and buildable by a small team.
```

---

## 19.23 README / Repository Prompt

Use this when starting the repo.

```text
Create a README.md for the repository of our Romanian SME AI operations companion.

The README should explain:
- what the project is
- product goal
- MVP scope
- architecture overview
- tech stack placeholders
- local development setup
- folder structure
- environment variables
- demo dataset
- AI workflow overview
- human approval principle
- security/privacy notes
- roadmap

Tone:
Clear, practical, developer-friendly.
Do not oversell.
```

---

## 19.24 Pilot Discovery Call Prompt

Use this when preparing customer interviews.

```text
Create a discovery call script for Romanian SME owners/managers who may test our AI Document & Operations Inbox.

Goal:
Understand their document/email/accountant workflow and determine whether our pilot is useful.

Generate:
1. Opening explanation.
2. 15 discovery questions.
3. Questions about invoices.
4. Questions about emails/client requests.
5. Questions about accountant communication.
6. Questions about contracts/documents.
7. Questions about current tools.
8. Questions about data/privacy concerns.
9. How to explain the pilot.
10. How to close the call.
11. Red flags that they are not a good pilot customer.

Keep it natural and non-salesy.
```

---

## 19.25 Outreach Email Prompt

Use this to contact early testers.

```text
Write a short outreach email in Romanian and English for Romanian SME owners/managers.

Context:
We are testing a private AI Document & Operations Inbox that helps with invoices, emails, contracts, accountant communication, and company knowledge.

Goal:
Invite them to a short discovery call or pilot.

Tone:
- human
- practical
- not spammy
- not hype-driven
- clear about being an early pilot

Include:
1. Subject lines.
2. Romanian version.
3. English version.
4. Short LinkedIn message version.
5. Follow-up message.
```

---

## 19.26 Security & Privacy Page Prompt

Use this to define trust language.

```text
Write the Security & Privacy page for our Romanian SME AI operations companion.

Important principles:
- AI prepares, humans approve.
- Company documents are private.
- Answers should be grounded in uploaded company context.
- Audit logs are important.
- EU/GDPR-aware design.
- Be honest about MVP vs planned features.

Create sections:
1. Our trust principle.
2. What data the system uses.
3. What the AI can and cannot do.
4. Human approval.
5. Audit trail.
6. Data storage direction.
7. GDPR-aware design.
8. MVP features vs planned features.
9. Customer responsibilities.
10. Contact for privacy questions.

Tone:
Transparent, calm, concrete.
Do not make legal guarantees unless clearly framed as goals or design principles.
```

---

## 19.27 Product Demo Video Script Prompt

Use this once mock UI exists.

```text
Write a 3-minute product demo video script for our Romanian SME AI operations companion.

Demo scenario:
Atelier Nova SRL has supplier invoices, client emails, an accountant request, and a contract.
The AI Document & Operations Inbox organizes the mess into clear next actions.

The script should include:
1. Opening problem.
2. Dashboard introduction.
3. AI Inbox walkthrough.
4. Invoice extraction example.
5. Ask My Company example.
6. Draft reply example.
7. Human approval explanation.
8. Pilot CTA.

Tone:
Clear, calm, practical, Romanian SME friendly.
Avoid hype.
```

---

## 19.28 Project Review Prompt

Use this after each phase.

```text
Review our current project state for the Romanian SME AI operations companion.

Inputs I will provide:
- current website copy
- current UI screenshots or description
- current architecture
- current backlog
- current demo flow

Evaluate:
1. Is the product clear?
2. Is the market wedge strong?
3. Is the website concrete enough?
4. Is the demo convincing?
5. Is the MVP too large?
6. What should be removed?
7. What should be built next?
8. What would confuse a Romanian SME buyer?
9. What proof is still missing?
10. What is the next best action?

Be direct and practical.
```

---

# 20. Recommended Prompt Sequence

Use the prompts in this order:

1. **Master Project Orchestrator Prompt**
2. **Product Identity Prompt**
3. **Target Customer Prompt**
4. **Product Offer Prompt**
5. **Website Structure Prompt**
6. **Homepage Copy Prompt**
7. **Product Page Prompt**
8. **Demo Workflow Prompt**
9. **Synthetic Dataset Prompt**
10. **Dashboard UX Prompt**
11. **Frontend Implementation Prompt**
12. **Technical Architecture Prompt**
13. **Backend MVP Prompt**
14. **MVP Backlog Prompt**
15. **Runtime AI Prompts**
16. **Evaluation Prompt**
17. **Pilot Discovery Prompt**
18. **Outreach Prompt**
19. **Project Review Prompt**

The most important sequence for immediate progress:

1. Product Identity
2. Website Structure
3. Homepage Copy
4. Demo Workflow
5. Synthetic Dataset
6. Dashboard UX
7. Frontend Mock

This gives us a visible product definition before deep backend work begins.

---

# 21. Practical Working Method

For each phase, use this loop:

1. Ask for the artifact with one of the prompts.
2. Review the output.
3. Simplify it.
4. Convert it into a website section, mock UI, code task, or runtime prompt.
5. Build only the next smallest useful piece.
6. Test it with the synthetic demo company.
7. Repeat.

Avoid trying to build the full system at once.

The project should move like this:

> Product clarity → website → mock demo → one real AI workflow → pilot conversation → product refinement.

This keeps the work grounded, visible, and market-testable.

---
