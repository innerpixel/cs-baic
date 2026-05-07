# UX Discoveries

Running log of friction points, gaps, and ideas found during manual testing.
Each entry: date · where found · observation · possible direction.

---

## 2026-05-07 — Contract Terms panel shows [object Object] (fixed)

**Where:** `/app/inbox` — ContractTermsPanel, Payment Terms / Penalties / Termination / Questions  
**Finding:** LLM returns structured objects `{"description": "...", "due_days": 14}` for list fields. Frontend expected plain strings. Showed `[object Object]` for every list item.  
**Fix:** Schema `_drop_nulls` now coerces dicts to their `description` field (or joins values). Prompt updated to explicitly require plain strings in all list fields.  
**Files:** `app/schemas/contract.py`, `app/prompts/contract_reviewer_v1.txt`

---

## 2026-05-07 — Contract analysis output (positive)

**Where:** `/app/inbox` — contract_supplier_lumina_design.pdf  
**Finding:** Contract reviewer correctly identified three real legal gaps in the demo contract:
- No total contract value or order cap defined
- Penalties only cover late payment (by buyer), not late delivery (by supplier)
- Renewal clause exists but has no defined process or timeline
**Signal:** Analyzer is producing genuinely useful output, not generic flags. Core value proposition works.

---

## 2026-05-07 — UX Analysis (full review)

### Critical friction

**Upload is the wrong mental model**
Form asks for pasted text + manual filename + manual type. Real users have files on disk. Should be drag-and-drop file upload. Classifier already detects type — the dropdown is redundant.

**Ask sources don't navigate to the document**
Clicking a source filename in /ask goes to /app/inbox but doesn't select that document. Must deep-link.

**No way to view the original document**
Once uploaded, raw text is not accessible. If the AI flags something missing, user can't verify against the source.

### Missing workflow pieces

**No reject / flag / comment on approval**
Only one button: Approve. Need at minimum: Approve / Needs Attention / Reject, plus a notes field.

**Due dates extracted but not surfaced**
Invoice extractor pulls due dates. No calendar view, no "due this week" filter, no sort by due date. Urgency badge exists but is passive — not actionable.

**No retry on failed analysis**
No retry button after failure. No way to re-run if wrong type was assigned.

**Language mismatch**
Interface in English, documents and company in Romanian. Summaries and suggested actions should match the user's language. Interface should eventually be in Romanian.

**Draft Reply only available for client_request**
Accountant requests also need drafted replies. Should work for accountant_request type too.

### Usability gaps

**No search or filter in document list**
Past 10–15 documents the sidebar is unusable. Needs filter by type and urgency at minimum.

**Processing feedback is opaque**
"Analyzing document…" gives no progress. Which analyzer? How long?

**Audit timeline uses internal event names**
`analysis_complete`, `analysis_failed` — not human-readable. Should read "AI analysis completed", "Approved by user".

**No document count or index status in Ask**
Users can't tell how many documents are indexed or whether a newly uploaded doc is searchable yet.

---

## 2026-05-07 — Inbox upload form

**Where:** `/app/inbox` upload form  
**Finding:** The upload form asks the user to paste text, type a filename, and select a document type manually. For the same effort, the user could just process the document themselves — the form adds no value over doing it manually.  
**Possible directions:**
- File drag-and-drop (upload the actual PDF/doc, extract text server-side — pipeline already supports this)
- Auto-detect document type instead of asking the user to select it — classifier analyzer already does this
- Remove the manual filename field — derive it from the uploaded file name
