# Business Companion AI

Private AI operations workspace for Romanian SMEs — documents, invoices, emails, contracts, and company knowledge in one intelligent workspace.

## Development

```sh
npm install
npm run dev
```

## Routes

- `/` — homepage (product overview, pilot offer)
- `/demo` — demo workflow with Atelier Nova SRL
- `/app/inbox` — mock AI Inbox (4 synthetic documents)

## Docs and coordination state

- `ops/project.state.hybrid` — current build slice and patchlog (start here)
- `ops/slice-1.homepage.hybrid` — this slice: scope, acceptance, builder prompt
- `ops/rules.constraints.hybrid` — durable constraints (palette, tone, data, stack)
- `romanian_sme_ai_companion_blueprint.md` — product vision and module definitions
- `romanian_sme_ai_companion_project_control_pack.md` — MVP boundary, demo company, prompt registry
- `romanian_sme_ai_companion_promotion_go_to_market_pack.md` — GTM messaging and channel plan

## Stack

SvelteKit · Svelte 5 · TypeScript · Tailwind v4

FastAPI backend joins in slice-3. Layout restructures to `apps/web` at that point.

## Demo data

All data in `src/lib/data/inbox.ts` is synthetic. Demo company: **Atelier Nova SRL** (Pitești, 12 employees). No real CUI, IBAN, name, or company data.
