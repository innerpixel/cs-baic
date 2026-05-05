<script lang="ts">
	import { INBOX_DOCS } from '$lib/data/inbox.js';
	import { DRAFT_REPLIES } from '$lib/data/replies.js';

	let selectedId = $state<string>(INBOX_DOCS[0].id);

	let selected = $derived(INBOX_DOCS.find((d) => d.id === selectedId) ?? INBOX_DOCS[0]);

	function urgencyColor(u: string) {
		if (u === 'High') return 'var(--color-urgency-high)';
		if (u === 'Medium') return 'var(--color-urgency-medium)';
		return 'var(--color-urgency-low)';
	}

	let approvalStates = $state<Record<string, string>>(
		Object.fromEntries(INBOX_DOCS.map((d) => [d.id, d.approval]))
	);

	function approve(id: string) {
		approvalStates[id] = 'Approved';
	}

	function archive(id: string) {
		approvalStates[id] = 'Archived';
	}

	// Draft Reply state per doc
	type DraftState = 'suggested' | 'editing' | 'approved' | 'discarded';
	let draftStates = $state<Record<string, DraftState>>({});
	let draftEdits = $state<Record<string, string>>({});
	let draftAuditEvents = $state<Record<string, { timestamp: string; event: string }[]>>({});

	function getDraftReply(docId: string) {
		return DRAFT_REPLIES.find((r) => r.docId === docId) ?? null;
	}

	function getDraftState(docId: string): DraftState {
		return draftStates[docId] ?? 'suggested';
	}

	function getDraftBody(docId: string): string {
		if (draftEdits[docId] !== undefined) return draftEdits[docId];
		return getDraftReply(docId)?.body ?? '';
	}

	function approveDraft(docId: string) {
		draftStates[docId] = 'approved';
		const ts = new Date().toISOString().slice(0, 16).replace('T', ' ');
		draftAuditEvents[docId] = [
			...(draftAuditEvents[docId] ?? []),
			{ timestamp: ts, event: 'Draft reply approved by user — ready to send manually' }
		];
	}

	function startEdit(docId: string) {
		if (draftEdits[docId] === undefined) {
			draftEdits[docId] = getDraftReply(docId)?.body ?? '';
		}
		draftStates[docId] = 'editing';
	}

	function discardDraft(docId: string) {
		draftStates[docId] = 'discarded';
		const ts = new Date().toISOString().slice(0, 16).replace('T', ' ');
		draftAuditEvents[docId] = [
			...(draftAuditEvents[docId] ?? []),
			{ timestamp: ts, event: 'Draft reply discarded by user' }
		];
	}
</script>

<svelte:head>
	<title>AI Inbox — Atelier Nova SRL — Business Companion AI</title>
</svelte:head>

<!-- SIDEBAR -->
<aside
	style="width: 280px; flex-shrink: 0; background: var(--color-data); border-right: 1px solid var(--color-stroke); overflow-y: auto; display: flex; flex-direction: column;"
>
	<div style="padding: 16px 16px 8px; border-bottom: 1px solid var(--color-stroke);">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 2px;">
			AI Inbox
		</div>
		<div style="font-size: 13px; color: var(--color-stroke-light);">
			{INBOX_DOCS.length} documents analyzed
		</div>
	</div>
	<nav style="padding: 8px 0; flex: 1;">
		{#each INBOX_DOCS as doc}
			<button
				onclick={() => (selectedId = doc.id)}
				style="width: 100%; text-align: left; background: {selectedId === doc.id
					? 'var(--color-main)'
					: 'transparent'}; border: none; border-left: 3px solid {selectedId === doc.id
					? 'var(--color-stroke-light)'
					: 'transparent'}; padding: 12px 16px; cursor: pointer; display: block;"
			>
				<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
					<span style="font-size: 11px; color: var(--color-text-muted); background: var(--color-action); padding: 1px 6px; border-radius: 2px;">
						{doc.type}
					</span>
					<span style="font-size: 11px; color: {urgencyColor(doc.urgency)}; font-weight: 600;">
						{doc.urgency}
					</span>
				</div>
				<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 4px; font-family: monospace; word-break: break-all; line-height: 1.3;">
					{doc.filename}
				</div>
				<div style="font-size: 12px; color: {approvalStates[doc.id] === 'Approved'
					? 'var(--color-urgency-low)'
					: approvalStates[doc.id] === 'Archived'
						? 'var(--color-text-muted)'
						: 'var(--color-urgency-medium)'};">
					{approvalStates[doc.id]}
				</div>
			</button>
		{/each}
	</nav>
	<div style="padding: 12px 16px; border-top: 1px solid var(--color-stroke);">
		<a href="/demo" style="font-size: 12px; color: var(--color-text-muted); text-decoration: none;">← Back to demo workflow</a>
	</div>
</aside>

<!-- MAIN DETAIL PANEL -->
<main style="flex: 1; overflow-y: auto; padding: 24px 28px; max-width: 900px;">
	<!-- Header -->
	<div style="margin-bottom: 24px;">
		<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap;">
			<span
				style="font-size: 12px; background: var(--color-action); color: var(--color-text-muted); padding: 3px 10px; border-radius: 3px;"
			>
				{selected.type}
			</span>
			<span style="font-size: 13px; font-weight: 600; color: {urgencyColor(selected.urgency)};">
				{selected.urgency} urgency
			</span>
			<span style="font-size: 12px; color: var(--color-text-muted); background: var(--color-main); padding: 3px 10px; border-radius: 3px; border: 1px solid var(--color-stroke);">
				{approvalStates[selected.id]}
			</span>
		</div>
		<div style="font-family: monospace; font-size: 13px; color: var(--color-stroke-light); margin-bottom: 4px;">
			{selected.filename}
		</div>
	</div>

	<!-- Summary -->
	<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px; margin-bottom: 16px;">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">
			AI Summary
		</div>
		<p style="font-size: 14px; color: var(--color-text); line-height: 1.6; margin: 0;">
			{selected.summary}
		</p>
	</section>

	<!-- Suggested action -->
	<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-left: 3px solid var(--color-stroke-light); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">
			Suggested Action
		</div>
		<p style="font-size: 14px; color: var(--color-text); line-height: 1.6; margin: 0;">
			{selected.suggestedAction}
		</p>
	</section>

	<!-- Fields + Missing + Risk flags row -->
	<div style="display: grid; grid-template-columns: 1fr {selected.missingFields.length > 0 || selected.riskFlags.length > 0 ? '280px' : '0px'}; gap: 16px; margin-bottom: 16px; align-items: start;">
		<!-- Extracted fields -->
		<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px;">
			<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">
				Extracted Fields
			</div>
			<dl style="margin: 0; display: flex; flex-direction: column; gap: 8px;">
				{#each selected.fields as field}
					<div style="display: flex; gap: 12px; align-items: flex-start;">
						<dt style="font-size: 12px; color: var(--color-text-muted); min-width: 140px; flex-shrink: 0; padding-top: 1px;">
							{field.label}
						</dt>
						<dd style="font-size: 13px; color: var(--color-text); margin: 0; line-height: 1.4;">
							{field.value}
						</dd>
					</div>
				{/each}
			</dl>
		</section>

		<!-- Missing + Risk flags -->
		{#if selected.missingFields.length > 0 || selected.riskFlags.length > 0}
			<div style="display: flex; flex-direction: column; gap: 12px;">
				{#if selected.missingFields.length > 0}
					<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-urgency-medium); border-radius: 8px; padding: 14px 16px;">
						<div style="font-size: 11px; color: var(--color-urgency-medium); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">
							Missing Information
						</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px;">
							{#each selected.missingFields as field}
								<li style="font-size: 13px; color: var(--color-text); display: flex; gap: 8px; align-items: flex-start;">
									<span style="color: var(--color-urgency-medium); margin-top: 1px; flex-shrink: 0;">!</span>
									{field}
								</li>
							{/each}
						</ul>
					</section>
				{/if}

				{#if selected.riskFlags.length > 0}
					<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-urgency-high); border-radius: 8px; padding: 14px 16px;">
						<div style="font-size: 11px; color: var(--color-urgency-high); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">
							Risk Flags
						</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px;">
							{#each selected.riskFlags as flag}
								<li style="font-size: 13px; color: var(--color-text); display: flex; gap: 8px; align-items: flex-start;">
									<span style="color: var(--color-urgency-high); margin-top: 1px; flex-shrink: 0;">▲</span>
									{flag}
								</li>
							{/each}
						</ul>
					</section>
				{/if}
			</div>
		{/if}
	</div>

	<!-- Approval controls -->
	<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">
			Human Approval
		</div>
		<p style="font-size: 13px; color: var(--color-text-muted); margin: 0 0 14px; line-height: 1.5;">
			AI has prepared the analysis above. Review it and decide the next step.
		</p>
		<div style="display: flex; gap: 10px; flex-wrap: wrap;">
			<button
				onclick={() => approve(selected.id)}
				disabled={approvalStates[selected.id] === 'Approved'}
				style="background: {approvalStates[selected.id] === 'Approved'
					? 'var(--color-urgency-low)'
					: 'var(--color-action)'}; color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 9px 20px; border-radius: 5px; font-size: 13px; cursor: {approvalStates[
					selected.id
				] === 'Approved'
					? 'default'
					: 'pointer'}; font-weight: 500;"
			>
				{approvalStates[selected.id] === 'Approved' ? '✓ Approved' : 'Approve'}
			</button>
			<button
				onclick={() => archive(selected.id)}
				disabled={approvalStates[selected.id] === 'Archived'}
				style="background: transparent; color: var(--color-text-muted); border: 1px solid var(--color-stroke); padding: 9px 20px; border-radius: 5px; font-size: 13px; cursor: {approvalStates[
					selected.id
				] === 'Archived'
					? 'default'
					: 'pointer'};"
			>
				{approvalStates[selected.id] === 'Archived' ? 'Archived' : 'Archive'}
			</button>
		</div>
	</section>

	<!-- Draft Reply panel — only for Client Request docs that have a canned reply -->
	{#if selected.type === 'Client Request' && getDraftReply(selected.id) !== null}
		{@const reply = getDraftReply(selected.id)!}
		{@const ds = getDraftState(selected.id)}
		<section
			style="background: var(--color-data); border: 1px solid var(--color-stroke); border-left: 3px solid var(--color-urgency-medium); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;"
		>
			<div
				style="font-size: 11px; color: var(--color-urgency-medium); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 10px;"
			>
				Draft Reply
				{#if ds === 'approved'}
					<span
						style="margin-left: 8px; color: var(--color-urgency-low); background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 3px; padding: 1px 7px; font-size: 10px;"
						>Approved</span
					>
				{/if}
			</div>

			{#if ds === 'discarded'}
				<p style="font-size: 13px; color: var(--color-text-muted); margin: 0;">
					Draft reply was discarded.
				</p>
			{:else}
				<div style="margin-bottom: 10px;">
					<div style="font-size: 11px; color: var(--color-text-muted); margin-bottom: 4px; letter-spacing: 0.04em; text-transform: uppercase;">
						Subject
					</div>
					<div style="font-size: 13px; color: var(--color-text);">{reply.subject}</div>
				</div>

				<div>
					<div style="font-size: 11px; color: var(--color-text-muted); margin-bottom: 6px; letter-spacing: 0.04em; text-transform: uppercase;">
						Body
					</div>
					{#if ds === 'editing'}
						<textarea
							bind:value={draftEdits[selected.id]}
							rows={14}
							style="width: 100%; background: var(--color-main); border: 1px solid var(--color-stroke-light); border-radius: 5px; padding: 10px 14px; font-size: 13px; color: var(--color-text); font-family: inherit; line-height: 1.6; resize: vertical; box-sizing: border-box; outline: none;"
						></textarea>
						<p style="font-size: 11px; color: var(--color-text-muted); margin: 6px 0 0;">
							Changes are local only — they will not be saved or sent.
						</p>
					{:else}
						<pre
							style="font-size: 13px; color: var(--color-text); font-family: inherit; white-space: pre-wrap; word-break: break-word; margin: 0; line-height: 1.65; background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 5px; padding: 12px 14px;"
						>{getDraftBody(selected.id)}</pre>
					{/if}
				</div>

				{#if ds !== 'approved'}
					<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px;">
						<button
							onclick={() => approveDraft(selected.id)}
							style="background: var(--color-urgency-low); color: var(--color-main); border: none; padding: 8px 18px; border-radius: 5px; font-size: 13px; cursor: pointer; font-weight: 500;"
						>
							Approve
						</button>
						{#if ds !== 'editing'}
							<button
								onclick={() => startEdit(selected.id)}
								style="background: var(--color-action); color: var(--color-text); border: 1px solid var(--color-stroke); padding: 8px 18px; border-radius: 5px; font-size: 13px; cursor: pointer;"
							>
								Edit locally
							</button>
						{/if}
						<button
							onclick={() => discardDraft(selected.id)}
							style="background: transparent; color: var(--color-text-muted); border: 1px solid var(--color-stroke); padding: 8px 18px; border-radius: 5px; font-size: 13px; cursor: pointer;"
						>
							Discard
						</button>
					</div>
				{:else}
					<p style="font-size: 13px; color: var(--color-urgency-low); margin: 12px 0 0;">
						Draft approved. Copy the text above and send it manually.
					</p>
				{/if}
			{/if}
		</section>
	{/if}

	<!-- Audit timeline -->
	<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">
			Audit Timeline
		</div>
		<div style="display: flex; flex-direction: column; gap: 0;">
			{#each selected.audit as event, i}
				<div style="display: flex; gap: 14px; align-items: flex-start; padding: 8px 0; {i < selected.audit.length - 1 ? 'border-bottom: 1px solid var(--color-stroke);' : ''}">
					<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: var(--color-stroke-light); margin-top: 5px;"></div>
					<div>
						<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 2px; font-family: monospace;">
							{event.timestamp}
						</div>
						<div style="font-size: 13px; color: var(--color-text);">{event.event}</div>
					</div>
				</div>
			{/each}
			{#if approvalStates[selected.id] === 'Approved'}
				<div style="display: flex; gap: 14px; align-items: flex-start; padding: 8px 0; border-top: 1px solid var(--color-stroke);">
					<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: var(--color-urgency-low); margin-top: 5px;"></div>
					<div>
						<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 2px; font-family: monospace;">
							{new Date().toISOString().slice(0, 16).replace('T', ' ')}
						</div>
						<div style="font-size: 13px; color: var(--color-text);">Human approved — action confirmed</div>
					</div>
				</div>
			{/if}
			{#if approvalStates[selected.id] === 'Archived'}
				<div style="display: flex; gap: 14px; align-items: flex-start; padding: 8px 0; border-top: 1px solid var(--color-stroke);">
					<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: var(--color-text-muted); margin-top: 5px;"></div>
					<div>
						<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 2px; font-family: monospace;">
							{new Date().toISOString().slice(0, 16).replace('T', ' ')}
						</div>
						<div style="font-size: 13px; color: var(--color-text-muted);">Archived by user</div>
					</div>
				</div>
			{/if}
			{#each (draftAuditEvents[selected.id] ?? []) as devt}
				<div style="display: flex; gap: 14px; align-items: flex-start; padding: 8px 0; border-top: 1px solid var(--color-stroke);">
					<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: var(--color-urgency-medium); margin-top: 5px;"></div>
					<div>
						<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 2px; font-family: monospace;">
							{devt.timestamp}
						</div>
						<div style="font-size: 13px; color: var(--color-text);">{devt.event}</div>
					</div>
				</div>
			{/each}
		</div>
	</section>

	<!-- Raw document content -->
	<details style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 14px 18px;">
		<summary style="font-size: 12px; color: var(--color-text-muted); cursor: pointer; letter-spacing: 0.04em; text-transform: uppercase; list-style: none;">
			▶ Original Document Text (Romanian)
		</summary>
		<pre
			style="margin: 14px 0 0; font-size: 12px; color: var(--color-text-muted); white-space: pre-wrap; word-break: break-word; font-family: monospace; line-height: 1.6; border-top: 1px solid var(--color-stroke); padding-top: 12px;"
		>{selected.rawContent}</pre>
	</details>
</main>
