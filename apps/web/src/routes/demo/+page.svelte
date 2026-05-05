<script lang="ts">
	const steps = [
		{
			number: '01',
			title: 'Documents arrive',
			description:
				'Atelier Nova SRL receives a supplier invoice (Lumina Design SRL), an accountant request, a client email about a design project, and a supplier contract — all through different channels.',
			detail: 'Invoice · Accountant email · Client email · Supplier contract',
			accent: false
		},
		{
			number: '02',
			title: 'AI creates Inbox cards',
			description:
				'Each document is classified automatically: type, language, urgency. The AI Inbox organizes them into structured cards ready for review.',
			detail: 'Supplier Invoice · Accountant Request · Client Request · Supplier Contract',
			accent: false
		},
		{
			number: '03',
			title: 'AI extracts key data',
			description:
				'For the invoice: supplier name, amount (3,046.40 RON), due date (12 May), and IBAN. For the contract: payment terms, delivery time, and penalty clauses.',
			detail: 'Amounts · Due dates · Parties · Obligations · Payment terms',
			accent: false
		},
		{
			number: '04',
			title: 'AI flags missing information',
			description:
				'The Lumina Design invoice is missing the internal purchase order reference. The client email is missing floor plan, budget, and style preferences before an offer can be prepared.',
			detail: 'Missing PO reference on invoice · Missing brief details from client',
			accent: true
		},
		{
			number: '05',
			title: 'AI suggests next actions',
			description:
				'For each document: a concrete suggested action. Ask for the missing PO reference. Collect the four documents the accountant needs by 10 May. Reply to the client with a brief request.',
			detail: 'Suggested action visible on every card',
			accent: false
		},
		{
			number: '06',
			title: 'Human reviews and approves',
			description:
				'Irina (owner manager) opens each card, reads the AI summary, checks the extracted fields, and decides: approve the suggested action, edit it, or archive the document.',
			detail: 'Approve · Edit · Archive — no autonomous decisions',
			accent: false
		},
		{
			number: '07',
			title: 'Action completed · Audit logged',
			description:
				'Every decision is recorded in the audit log: what the AI suggested, what the human approved, and when. The document moves to the next status: reviewed, approved, or done.',
			detail: 'Full audit trail · Source references · Human approval marker',
			accent: false
		}
	];

	const inboxCards = [
		{
			filename: 'invoice_lumina_design_2026_0041.pdf',
			type: 'Supplier Invoice',
			urgency: 'High',
			summary: 'LED panels and accessories — 3,046.40 RON — due 12.05.2026',
			flag: 'Missing PO reference'
		},
		{
			filename: 'email_accountant_missing_docs_april.txt',
			type: 'Accountant Request',
			urgency: 'High',
			summary: '4 documents requested by Mihai — deadline 10 May',
			flag: 'Deadline in 5 days'
		},
		{
			filename: 'email_client_apartament_bucuresti.txt',
			type: 'Client Request',
			urgency: 'Medium',
			summary: 'Design offer for 78 sqm apartment in Bucharest — June start',
			flag: 'Missing brief'
		},
		{
			filename: 'contract_supplier_lumina_design.txt',
			type: 'Supplier Contract',
			urgency: 'Low',
			summary: 'Collaboration contract — valid to 31.12.2026 — 3 risk flags',
			flag: 'Payment penalties clause'
		}
	];
</script>

<svelte:head>
	<title>Demo Workflow — Business Companion AI</title>
	<meta
		name="description"
		content="See how Business Companion AI processes invoices, emails, contracts, and accountant requests for a Romanian SME."
	/>
</svelte:head>

<!-- NAV -->
<nav style="background: var(--color-data); border-bottom: 1px solid var(--color-stroke);">
	<div
		style="max-width: 1100px; margin: 0 auto; padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between;"
	>
		<a href="/" style="color: var(--color-text); text-decoration: none; font-weight: 600; font-size: 15px;">
			Business Companion AI
		</a>
		<div style="display: flex; gap: 24px; align-items: center;">
			<a href="/demo" style="color: var(--color-text); text-decoration: none; font-size: 14px; font-weight: 500;">
				Demo
			</a>
			<a href="/app/inbox" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">
				AI Inbox
			</a>
			<a
				href="mailto:ned.gabrielc@gmail.com?subject=Business Companion AI — Pilot Request"
				style="background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 7px 16px; border-radius: 5px; font-size: 13px; border: 1px solid var(--color-stroke);"
			>
				Request a Pilot
			</a>
		</div>
	</div>
</nav>

<!-- HEADER -->
<section style="max-width: 1100px; margin: 0 auto; padding: 56px 24px 40px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Demo workflow · Atelier Nova SRL
	</p>
	<h1 style="font-size: clamp(24px, 4vw, 36px); font-weight: 700; color: var(--color-text); margin: 0 0 16px; max-width: 640px; line-height: 1.25;">
		From messy documents to clear next actions
	</h1>
	<p style="color: var(--color-text-muted); font-size: 16px; line-height: 1.6; max-width: 600px; margin: 0 0 32px;">
		A Romanian SME receives supplier invoices, a client request, and an accountant email. The AI
		Companion reads everything, classifies the items, extracts important information, and shows what
		needs human approval.
	</p>
	<div
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 18px; display: inline-flex; gap: 24px; font-size: 13px; color: var(--color-text-muted); flex-wrap: wrap;"
	>
		<span>Demo company: <strong style="color: var(--color-text);">Atelier Nova SRL</strong></span>
		<span>4 documents processed</span>
		<span>All data synthetic</span>
		<span>Under 3 minutes</span>
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- WORKFLOW STEPS -->
<section style="max-width: 1100px; margin: 0 auto; padding: 48px 24px;">
	<div style="display: flex; flex-direction: column; gap: 4px;">
		{#each steps as step, i}
			<div
				style="display: flex; gap: 24px; padding: 24px 0; border-bottom: 1px solid var(--color-stroke); {i === 0
					? 'border-top: 1px solid var(--color-stroke);' : ''}"
			>
				<div
					style="flex-shrink: 0; width: 48px; height: 48px; background: {step.accent
						? 'var(--color-action)'
						: 'var(--color-main)'}; border: 1px solid var(--color-stroke); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; color: var(--color-text-muted); margin-top: 2px;"
				>
					{step.number}
				</div>
				<div style="flex: 1;">
					<h3 style="font-size: 16px; font-weight: 600; color: var(--color-text); margin: 0 0 8px;">
						{step.title}
					</h3>
					<p style="font-size: 14px; color: var(--color-text-muted); line-height: 1.6; margin: 0 0 10px; max-width: 640px;">
						{step.description}
					</p>
					<div
						style="font-size: 12px; color: var(--color-stroke-light); background: var(--color-data); border-radius: 4px; padding: 4px 10px; display: inline-block;"
					>
						{step.detail}
					</div>
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- MOCK INBOX CARDS PREVIEW -->
<section
	style="background: var(--color-main); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 48px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
			The AI Inbox after processing
		</p>
		<p style="color: var(--color-text-muted); font-size: 13px; margin-bottom: 28px;">
			These are the 4 cards generated for Atelier Nova SRL. Click "Open AI Inbox" to explore them.
		</p>
		<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 28px;">
			{#each inboxCards as card}
				<div
					style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 18px;"
				>
					<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
						<span
							style="font-size: 11px; background: var(--color-action); color: var(--color-text-muted); padding: 2px 8px; border-radius: 3px;"
						>
							{card.type}
						</span>
						<span
							style="font-size: 11px; color: {card.urgency === 'High'
								? 'var(--color-urgency-high)'
								: card.urgency === 'Medium'
									? 'var(--color-urgency-medium)'
									: 'var(--color-urgency-low)'}; font-weight: 600;"
						>
							{card.urgency}
						</span>
					</div>
					<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 6px; font-family: monospace;">
						{card.filename}
					</div>
					<div style="font-size: 13px; color: var(--color-text); line-height: 1.5; margin-bottom: 10px;">
						{card.summary}
					</div>
					<div
						style="font-size: 11px; color: var(--color-urgency-medium); background: var(--color-data); padding: 3px 8px; border-radius: 3px; display: inline-block;"
					>
						⚠ {card.flag}
					</div>
				</div>
			{/each}
		</div>
		<a
			href="/app/inbox"
			style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 11px 22px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke-light);"
		>
			Open AI Inbox →
		</a>
	</div>
</section>

<!-- CTA -->
<section style="max-width: 1100px; margin: 0 auto; padding: 56px 24px;">
	<div style="max-width: 520px;">
		<h2 style="font-size: 22px; font-weight: 600; color: var(--color-text); margin: 0 0 12px;">
			Test one workflow in your company.
		</h2>
		<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.6; margin: 0 0 24px;">
			The pilot starts with one small workflow, not a full platform. 14 days, anonymized documents,
			clear results.
		</p>
		<a
			href="mailto:ned.gabrielc@gmail.com?subject=Business Companion AI — Pilot Request"
			style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke-light); font-weight: 500;"
		>
			Request a Pilot
		</a>
	</div>
</section>
