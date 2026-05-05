<script lang="ts">
	const modules = [
		{
			icon: '📥',
			name: 'AI Inbox',
			description:
				'Every uploaded document becomes a structured card: type, summary, extracted fields, urgency, and suggested next action.'
		},
		{
			icon: '💬',
			name: 'Ask My Company',
			description:
				'Ask questions about your documents. Answers come only from your uploaded company content — not from the internet.'
		},
		{
			icon: '✉️',
			name: 'Draft Reply Assistant',
			description:
				'AI prepares reply drafts for client emails, supplier messages, and accountant requests. You review before anything is sent.'
		},
		{
			icon: '🔍',
			name: 'Document Extraction',
			description:
				'Structured extraction from invoices, contracts, and emails: amounts, due dates, parties, obligations, missing fields.'
		},
		{
			icon: '✅',
			name: 'Human Approval',
			description:
				'Every AI suggestion waits for your approval. No autonomous sending. No silent decisions. You stay in control.'
		},
		{
			icon: '📋',
			name: 'Audit Log',
			description:
				'Every AI output and human decision is recorded. You can always trace what happened, when, and why.'
		}
	];

	const pains = [
		'Too many documents arriving through too many channels',
		'Invoice due dates and missing fields discovered too late',
		'Accountant keeps requesting documents that are hard to find',
		'Client emails waiting days for a reply',
		'Contract terms forgotten until a problem appears',
		'No clear view of what needs attention this week'
	];
</script>

<svelte:head>
	<title>Business Companion AI — AI Inbox for Romanian SMEs</title>
	<meta
		name="description"
		content="Business Companion AI turns scattered invoices, emails, contracts, and accountant requests into clear, human-approved next actions."
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
			<a href="/demo" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">
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

<!-- HERO -->
<section
	style="max-width: 1100px; margin: 0 auto; padding: 80px 24px 64px;"
>
	<div style="max-width: 680px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">
			For Romanian SMEs · Private AI workspace
		</p>
		<h1 style="font-size: clamp(28px, 5vw, 44px); font-weight: 700; line-height: 1.2; color: var(--color-text); margin: 0 0 20px;">
			Your company documents, emails, invoices, and contracts — organized by a private AI companion.
		</h1>
		<p style="font-size: 17px; color: var(--color-text-muted); line-height: 1.6; margin: 0 0 36px;">
			Built for Romanian SMEs that want less paperwork, faster replies, and safer access to company
			knowledge.
		</p>
		<div style="display: flex; gap: 12px; flex-wrap: wrap;">
			<a
				href="mailto:ned.gabrielc@gmail.com?subject=Business Companion AI — Pilot Request"
				style="background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke-light); font-weight: 500;"
			>
				Request a Pilot
			</a>
			<a
				href="/demo"
				style="background: transparent; color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke);"
			>
				See Example Workflow
			</a>
		</div>
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- PROBLEM -->
<section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		The problem
	</p>
	<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 32px; max-width: 560px;">
		Stop losing time in invoices, emails, contracts, and accountant requests.
	</h2>
	<ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
		{#each pains as pain}
			<li
				style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 16px; display: flex; gap: 10px; align-items: flex-start;"
			>
				<span style="color: var(--color-stroke-light); margin-top: 2px; flex-shrink: 0;">—</span>
				<span style="color: var(--color-text); font-size: 14px; line-height: 1.5;">{pain}</span>
			</li>
		{/each}
	</ul>
</section>

<!-- WHAT IT DOES -->
<section
	style="background: var(--color-main); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
			What it does
		</p>
		<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 12px;">
			Business Companion AI turns scattered documents into clear next actions.
		</h2>
		<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.6; max-width: 600px; margin: 0 0 40px;">
			Upload an invoice, email, contract, or accountant request. The AI classifies it, summarizes it,
			extracts key information, flags what is missing, and suggests what to do next. You review and
			approve.
		</p>
		<div
			style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px;"
		>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Step 1</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">Upload document</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Invoice, email, contract, or accountant request — any format.
				</div>
			</div>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Step 2</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">AI creates an Inbox card</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Classification, summary, extracted fields, urgency, and suggested action.
				</div>
			</div>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Step 3</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">Human reviews and approves</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Nothing is sent or acted on automatically. You decide.
				</div>
			</div>
		</div>
	</div>
</section>

<!-- DEMO WORKFLOW PREVIEW -->
<section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Demo workflow
	</p>
	<div
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 28px 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;"
	>
		<div style="max-width: 440px;">
			<h2 style="font-size: 20px; font-weight: 600; color: var(--color-text); margin: 0 0 10px;">
				See the full workflow with Atelier Nova SRL
			</h2>
			<p style="color: var(--color-text-muted); font-size: 14px; line-height: 1.6; margin: 0 0 20px;">
				A Romanian interior design company receives a supplier invoice, an accountant request, a
				client email, and a supplier contract. The AI Inbox processes everything in one workspace.
			</p>
			<a
				href="/demo"
				style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke-light);"
			>
				See Demo Workflow
			</a>
		</div>
		<div
			style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 16px 20px; min-width: 240px;"
		>
			<div style="font-size: 12px; color: var(--color-text-muted); margin-bottom: 12px; letter-spacing: 0.05em; text-transform: uppercase;">Demo company</div>
			<div style="font-weight: 600; color: var(--color-text); margin-bottom: 4px;">Atelier Nova SRL</div>
			<div style="font-size: 13px; color: var(--color-text-muted);">Interior design · Pitești · 12 employees</div>
			<hr style="border: none; border-top: 1px solid var(--color-stroke); margin: 12px 0;" />
			<div style="font-size: 13px; color: var(--color-text-muted); line-height: 1.7;">
				4 documents analyzed<br />
				All data synthetic
			</div>
		</div>
	</div>
</section>

<!-- MODULES -->
<section
	style="background: var(--color-data); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
			Modules
		</p>
		<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 32px;">
			One workspace. Six capabilities.
		</h2>
		<div
			style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;"
		>
			{#each modules as mod}
				<div
					style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 20px;"
				>
					<div style="font-size: 22px; margin-bottom: 10px;">{mod.icon}</div>
					<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px; font-size: 15px;">{mod.name}</div>
					<div style="font-size: 13px; color: var(--color-text-muted); line-height: 1.6;">{mod.description}</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- TRUST & PRIVACY -->
<section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Trust &amp; privacy
	</p>
	<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 12px;">
		AI prepares. Humans approve. Your data stays grounded in your own documents.
	</h2>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.6; max-width: 600px; margin: 0 0 36px;">
		Every AI output is a suggestion, not an action. Amounts, due dates, and obligations must be
		reviewed before any decision. The audit log records every step.
	</p>
	<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
		{#each [
			{ label: 'No autonomous sending', note: 'Available in MVP' },
			{ label: 'Human approval required', note: 'Available in MVP' },
			{ label: 'Audit log for every action', note: 'Available in MVP' },
			{ label: 'Answers grounded in your documents', note: 'Available in MVP' },
			{ label: 'EU hosting option', note: 'Planned' },
			{ label: 'Private deployment', note: 'Enterprise option' }
		] as item}
			<div
				style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 16px;"
			>
				<div style="font-size: 14px; color: var(--color-text); margin-bottom: 4px;">{item.label}</div>
				<div
					style="font-size: 11px; color: var(--color-text-muted); padding: 2px 7px; background: var(--color-action); border-radius: 3px; display: inline-block;"
				>
					{item.note}
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- PILOT OFFER -->
<section
	style="background: var(--color-main); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
			Pilot offer
		</p>
		<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 40px;">
			<div style="max-width: 480px;">
				<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 12px;">
					14-Day AI Operations Pilot
				</h2>
				<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.6; margin: 0 0 20px;">
					Start with one workflow. Test safely before committing to a larger system.
				</p>
				<ul style="list-style: none; padding: 0; margin: 0 0 28px; display: flex; flex-direction: column; gap: 8px;">
					{#each [
						'One company workspace configured',
						'AI Inbox demo with your document types',
						'Classification, summary, and extraction shown',
						'Human approval flow demonstrated',
						'Final report: which workflows are worth automating'
					] as item}
						<li style="display: flex; gap: 10px; align-items: flex-start;">
							<span style="color: var(--color-stroke-light); margin-top: 2px;">✓</span>
							<span style="font-size: 14px; color: var(--color-text);">{item}</span>
						</li>
					{/each}
				</ul>
				<a
					href="mailto:ned.gabrielc@gmail.com?subject=Business Companion AI — Pilot Request"
					style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke-light); font-weight: 500;"
				>
					Request a Pilot
				</a>
			</div>
			<div
				style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 24px 28px; min-width: 260px;"
			>
				<div style="font-size: 12px; color: var(--color-text-muted); margin-bottom: 16px; letter-spacing: 0.05em; text-transform: uppercase;">Pilot outcome</div>
				{#each [
					'Document map',
					'Workflow map',
					'AI readiness score',
					'List of automations worth building',
					'Demo workspace'
				] as outcome}
					<div style="display: flex; gap: 8px; align-items: center; margin-bottom: 10px;">
						<span style="color: var(--color-stroke-light); font-size: 12px;">→</span>
						<span style="font-size: 14px; color: var(--color-text);">{outcome}</span>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<!-- CONTACT / FOOTER -->
<footer style="max-width: 1100px; margin: 0 auto; padding: 40px 24px;">
	<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
		<div>
			<div style="font-weight: 600; color: var(--color-text); margin-bottom: 4px;">Business Companion AI</div>
			<div style="font-size: 13px; color: var(--color-text-muted);">Private AI operations workspace for Romanian SMEs.</div>
		</div>
		<div style="display: flex; gap: 20px; align-items: center;">
			<a href="/demo" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Demo</a>
			<a href="/app/inbox" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">AI Inbox</a>
			<a
				href="mailto:ned.gabrielc@gmail.com?subject=Business Companion AI — Contact"
				style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;"
			>
				Contact
			</a>
		</div>
	</div>
</footer>
