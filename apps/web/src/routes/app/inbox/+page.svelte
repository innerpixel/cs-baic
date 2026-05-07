<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type ApiDocumentDetail, type ApiDocumentItem } from '$lib/api/client.js';
	import ClassifierBadge from '$lib/components/ClassifierBadge.svelte';
	import ContractTermsPanel from '$lib/components/ContractTermsPanel.svelte';
	import DraftReplyPanel from '$lib/components/DraftReplyPanel.svelte';

	// ── State ────────────────────────────────────────────────────────────────

	let docs = $state<ApiDocumentItem[]>([]);
	let selected = $state<ApiDocumentDetail | null>(null);
	let selectedId = $state<string | null>(null);

	let loading = $state(true);
	let loadError = $state<string | null>(null);
	let detailLoading = $state(false);

	// upload form
	let uploadFile = $state<File | null>(null);
	let dragOver = $state(false);
	let pasteFallbackOpen = $state(false);
	let uploadText = $state('');
	let uploadFilename = $state('');
	let uploading = $state(false);
	let uploadError = $state<string | null>(null);
	let fileInputEl = $state<HTMLInputElement | null>(null);

	// local approval overlay (mirrors API state, refreshed on re-fetch)
	let localApproved = $state<Set<string>>(new Set());

	const DOC_TYPES = [
		{ value: 'supplier_invoice', label: 'Supplier Invoice' },
		{ value: 'client_invoice', label: 'Client Invoice' },
		{ value: 'contract', label: 'Contract' },
		{ value: 'supplier_offer', label: 'Supplier Offer' },
		{ value: 'client_request', label: 'Client Request' },
		{ value: 'accountant_request', label: 'Accountant Request' },
		{ value: 'hr_document', label: 'HR Document' },
		{ value: 'internal_procedure', label: 'Internal Procedure' },
		{ value: 'price_list', label: 'Price List' },
		{ value: 'unknown', label: 'Unknown' }
	];

	// ── Helpers ───────────────────────────────────────────────────────────────

	function typeLabel(apiType: string) {
		return DOC_TYPES.find((t) => t.value === apiType)?.label ?? apiType;
	}

	function statusColor(status: string) {
		if (status === 'done') return 'var(--color-urgency-low)';
		if (status === 'failed') return 'var(--color-urgency-high)';
		return 'var(--color-urgency-medium)';
	}

	function fmtDate(iso: string) {
		return iso.replace('T', ' ').slice(0, 16);
	}

	function eventLabel(event_type: string) {
		return event_type.replace(/_/g, ' ').replace(/:/g, ' · ');
	}

	function urgencyColor(urgency: string | null | undefined) {
		if (urgency === 'high') return 'var(--color-urgency-high)';
		if (urgency === 'medium') return 'var(--color-urgency-medium)';
		if (urgency === 'low') return 'var(--color-urgency-low)';
		return 'var(--color-text-muted)';
	}

	interface ExtractedField {
		label: string;
		value: string;
	}

	const FIELD_LABELS: Record<string, string> = {
		supplier_name: 'Supplier',
		supplier_cui: 'CUI Furnizor',
		supplier_vat_number: 'VAT Number',
		invoice_number: 'Invoice Number',
		invoice_date: 'Invoice Date',
		due_date: 'Due Date',
		total_amount: 'Total Amount',
		vat_amount: 'VAT Amount',
		currency: 'Currency',
		iban: 'IBAN',
		payment_status: 'Payment Status'
	};

	function extractionFields(fields: Record<string, unknown> | null): ExtractedField[] {
		if (!fields) return [];
		return Object.entries(FIELD_LABELS)
			.filter(([key]) => fields[key] != null && fields[key] !== '')
			.map(([key, label]) => ({ label, value: String(fields[key]) }));
	}

	// ── Data loading ──────────────────────────────────────────────────────────

	async function loadList() {
		try {
			docs = await api.listDocuments();
			loadError = null;
			if (!selectedId && docs.length > 0) {
				await selectDoc(docs[0].id);
			}
		} catch (e) {
			loadError = String(e);
		} finally {
			loading = false;
		}
	}

	async function selectDoc(id: string) {
		selectedId = id;
		detailLoading = true;
		try {
			selected = await api.getDocument(id);
		} catch {
			selected = null;
		} finally {
			detailLoading = false;
		}
	}

	// ── Actions ───────────────────────────────────────────────────────────────

	function onDragOver(e: DragEvent) {
		e.preventDefault();
		dragOver = true;
	}

	function onDragLeave() {
		dragOver = false;
	}

	function onDrop(e: DragEvent) {
		e.preventDefault();
		dragOver = false;
		const file = e.dataTransfer?.files?.[0];
		if (file) uploadFile = file;
	}

	function onFileChange(e: Event) {
		const input = e.target as HTMLInputElement;
		uploadFile = input.files?.[0] ?? null;
	}

	async function handleUpload(e: Event) {
		e.preventDefault();
		const canSubmit = uploadFile != null || (pasteFallbackOpen && uploadText.trim());
		if (!canSubmit) return;
		uploading = true;
		uploadError = null;
		try {
			const input = uploadFile
				? { file: uploadFile }
				: { text: uploadText, filename: uploadFilename.trim() || `pasted_${Date.now()}.txt` };
			const result = await api.uploadDocument(input);

			const displayName = uploadFile ? uploadFile.name : (uploadFilename.trim() || 'pasted.txt');
			uploadFile = null;
			uploadText = '';
			uploadFilename = '';
			pasteFallbackOpen = false;
			if (fileInputEl) fileInputEl.value = '';

			docs = [
				{
					id: result.id,
					filename: displayName,
					type: 'unknown',
					status: result.status === 'not_supported_yet' ? 'not_supported_yet' : 'queued',
					created_at: new Date().toISOString()
				},
				...docs
			];
			await selectDoc(result.id);
			if (result.status !== 'not_supported_yet') pollDoc(result.id);
		} catch (e) {
			uploadError = String(e);
		} finally {
			uploading = false;
		}
	}

	async function pollDoc(id: string, attempts = 0) {
		if (attempts > 30) return; // max 60s
		await new Promise((r) => setTimeout(r, 2000));
		try {
			const detail = await api.getDocument(id);
			// update list entry status
			docs = docs.map((d) => (d.id === id ? { ...d, status: detail.status } : d));
			if (selectedId === id) selected = detail;
			if (detail.status === 'done' || detail.status === 'failed') return;
		} catch {
			// ignore transient errors during polling
		}
		pollDoc(id, attempts + 1);
	}

	async function approveDoc(id: string) {
		try {
			await api.approveDocument(id);
			localApproved = new Set([...localApproved, id]);
			if (selectedId === id) {
				selected = await api.getDocument(id);
			}
		} catch (e) {
			console.error('Approve failed:', e);
		}
	}

	onMount(loadList);
</script>

<svelte:head>
	<title>AI Inbox — Atelier Nova SRL — Business Companion AI</title>
</svelte:head>

<!-- SIDEBAR -->
<aside
	style="width: 300px; flex-shrink: 0; background: var(--color-data); border-right: 1px solid var(--color-stroke); overflow-y: auto; display: flex; flex-direction: column;"
>
	<div style="padding: 16px 16px 8px; border-bottom: 1px solid var(--color-stroke);">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 2px;">
			AI Inbox
		</div>
		<div style="font-size: 13px; color: var(--color-stroke-light);">
			{loading ? 'Loading…' : loadError ? 'Error loading' : `${docs.length} documents`}
		</div>
	</div>

	<!-- Upload form -->
	<div style="padding: 12px 16px; border-bottom: 1px solid var(--color-stroke);">
		<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">
			Upload Document
		</div>
		<form onsubmit={handleUpload} style="display: flex; flex-direction: column; gap: 8px;">

			<!-- Drop zone -->
			<input
				bind:this={fileInputEl}
				type="file"
				accept=".pdf,.txt,application/pdf,text/plain"
				onchange={onFileChange}
				style="display: none;"
			/>
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div
				role="button"
				tabindex="0"
				onclick={() => fileInputEl?.click()}
				ondragover={onDragOver}
				ondragleave={onDragLeave}
				ondrop={onDrop}
				onkeydown={(e) => e.key === 'Enter' && fileInputEl?.click()}
				style="border: 2px dashed {dragOver ? 'var(--color-stroke-light)' : 'var(--color-stroke)'}; border-radius: 6px; padding: 20px 12px; text-align: center; cursor: pointer; background: {dragOver ? 'var(--color-action)' : 'transparent'}; transition: background 0.15s, border-color 0.15s;"
			>
				{#if uploadFile}
					<div style="font-size: 12px; color: var(--color-text); line-height: 1.5;">
						{uploadFile.name}<br />
						<span style="color: var(--color-text-muted);">{(uploadFile.size / 1024).toFixed(0)} KB</span>
					</div>
				{:else}
					<div style="font-size: 12px; color: var(--color-text-muted); line-height: 1.6;">
						Drop a PDF or text file<br />
						<span style="font-size: 11px;">or click to browse</span>
					</div>
				{/if}
			</div>

			<!-- Paste fallback -->
			<button
				type="button"
				onclick={() => (pasteFallbackOpen = !pasteFallbackOpen)}
				style="background: none; border: none; padding: 0; font-size: 11px; color: var(--color-text-muted); cursor: pointer; text-align: left; text-decoration: underline;"
			>
				{pasteFallbackOpen ? 'Hide paste option' : 'Or paste text…'}
			</button>
			{#if pasteFallbackOpen}
				<textarea
					bind:value={uploadText}
					placeholder="Paste document text here…"
					rows={4}
					style="width: 100%; background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 8px; font-size: 12px; color: var(--color-text); font-family: inherit; resize: vertical; box-sizing: border-box; outline: none;"
				></textarea>
				<input
					bind:value={uploadFilename}
					placeholder="filename.txt (optional)"
					style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 7px 8px; font-size: 12px; color: var(--color-text); outline: none; font-family: monospace;"
				/>
			{/if}

			<button
				type="submit"
				disabled={uploading || (!uploadFile && !(pasteFallbackOpen && uploadText.trim()))}
				style="background: var(--color-action); color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 8px; border-radius: 4px; font-size: 12px; cursor: pointer; font-weight: 500; opacity: {uploading ? 0.6 : 1};"
			>
				{uploading ? 'Uploading…' : 'Submit'}
			</button>

			{#if uploadError}
				<div style="font-size: 11px; color: var(--color-urgency-high); line-height: 1.4;">
					{uploadError.includes('not_supported_yet')
						? 'Could not extract text — likely an image-only PDF.'
						: uploadError}
				</div>
			{/if}
		</form>
	</div>

	<!-- Document list -->
	<nav style="padding: 8px 0; flex: 1; overflow-y: auto;">
		{#if loading}
			<div style="padding: 20px 16px; font-size: 13px; color: var(--color-text-muted);">
				Loading documents…
			</div>
		{:else if loadError}
			<div style="padding: 16px; font-size: 12px; color: var(--color-urgency-high); line-height: 1.5;">
				Could not reach API.<br />
				<span style="color: var(--color-text-muted);">Start the backend and refresh.</span>
			</div>
		{:else if docs.length === 0}
			<div style="padding: 20px 16px; font-size: 13px; color: var(--color-text-muted);">
				No documents yet. Upload one above.
			</div>
		{:else}
			{#each docs as doc}
				<button
					onclick={() => selectDoc(doc.id)}
					style="width: 100%; text-align: left; background: {selectedId === doc.id
						? 'var(--color-main)'
						: 'transparent'}; border: none; border-left: 3px solid {selectedId === doc.id
						? 'var(--color-stroke-light)'
						: 'transparent'}; padding: 12px 16px; cursor: pointer; display: block;"
				>
					<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
						<span style="font-size: 11px; color: var(--color-text-muted); background: var(--color-action); padding: 1px 6px; border-radius: 2px;">
							{typeLabel(doc.type)}
						</span>
						<span style="font-size: 10px; color: var(--color-urgency-low); background: var(--color-data); border: 1px solid var(--color-stroke); padding: 1px 5px; border-radius: 2px; font-weight: 600; letter-spacing: 0.05em;">
							LIVE
						</span>
					</div>
					<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 4px; font-family: monospace; word-break: break-all; line-height: 1.3;">
						{doc.filename}
					</div>
					<div style="display: flex; gap: 8px; align-items: center;">
						<span style="font-size: 12px; color: {statusColor(doc.status)};">{doc.status}</span>
					</div>
				</button>
			{/each}
		{/if}
	</nav>
	<div style="padding: 12px 16px; border-top: 1px solid var(--color-stroke);">
		<a href="/demo" style="font-size: 12px; color: var(--color-text-muted); text-decoration: none;">← Back to demo workflow</a>
	</div>
</aside>

<!-- MAIN DETAIL PANEL -->
<main style="flex: 1; overflow-y: auto; padding: 24px 28px; max-width: 900px;">
	{#if !selectedId || (!selected && !detailLoading)}
		<div style="display: flex; align-items: center; justify-content: center; height: 200px; color: var(--color-text-muted); font-size: 14px;">
			{loadError ? 'API unavailable — start the backend to use the live inbox.' : 'Select or upload a document.'}
		</div>
	{:else if detailLoading}
		<div style="display: flex; align-items: center; justify-content: center; height: 200px; color: var(--color-text-muted); font-size: 14px;">
			Loading…
		</div>
	{:else if selected}
		<!-- Header -->
		<div style="margin-bottom: 24px;">
			<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap;">
				<span style="font-size: 12px; background: var(--color-action); color: var(--color-text-muted); padding: 3px 10px; border-radius: 3px;">
					{typeLabel(selected.type)}
				</span>
				<span style="font-size: 11px; color: var(--color-urgency-low); background: var(--color-data); border: 1px solid var(--color-stroke); padding: 2px 8px; border-radius: 3px; font-weight: 600; letter-spacing: 0.05em;">
					LIVE
				</span>
				<span style="font-size: 12px; color: {statusColor(selected.status)}; background: var(--color-main); padding: 3px 10px; border-radius: 3px; border: 1px solid var(--color-stroke);">
					{selected.status}
				</span>
				{#if selected.analysis?.urgency && selected.analysis.urgency !== 'unknown'}
					<span style="font-size: 11px; color: {urgencyColor(selected.analysis.urgency)}; background: var(--color-data); border: 1px solid var(--color-stroke); padding: 2px 8px; border-radius: 3px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
						{selected.analysis.urgency}
					</span>
				{/if}
				{#if selected.analysis}
					<ClassifierBadge
						detectedType={selected.analysis.detected_type}
						docType={selected.type}
						confidence={selected.analysis.confidence}
					/>
				{/if}
			</div>
			<div style="font-family: monospace; font-size: 13px; color: var(--color-stroke-light); margin-bottom: 4px;">
				{selected.filename}
			</div>
		</div>

		<!-- Analysis (when available) -->
		{#if selected.status === 'queued' || selected.status === 'processing'}
			<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px; margin-bottom: 16px;">
				<p style="font-size: 14px; color: var(--color-text-muted); margin: 0;">
					Analyzing document… this usually takes a few seconds.
				</p>
			</section>
		{:else if selected.analysis}
			{@const fields = extractionFields(selected.analysis.fields)}
			{@const missing = selected.analysis.missing_fields ?? []}
			{@const flags = selected.analysis.risk_flags ?? []}

			{#if selected.analysis.summary}
				<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px; margin-bottom: 16px;">
					<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">AI Summary</div>
					<p style="font-size: 14px; color: var(--color-text); line-height: 1.6; margin: 0;">{selected.analysis.summary}</p>
				</section>
			{/if}

			{#if selected.analysis.suggested_action}
				<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-left: 3px solid var(--color-stroke-light); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
					<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">Suggested Action</div>
					<p style="font-size: 14px; color: var(--color-text); line-height: 1.6; margin: 0;">{selected.analysis.suggested_action}</p>
				</section>
			{/if}

			<!-- Fields + Missing + Risk flags row -->
			<div style="display: grid; grid-template-columns: 1fr {missing.length > 0 || flags.length > 0 ? '280px' : '0px'}; gap: 16px; margin-bottom: 16px; align-items: start;">
				{#if fields.length > 0}
					<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px;">
						<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">Extracted Fields</div>
						<dl style="margin: 0; display: flex; flex-direction: column; gap: 8px;">
							{#each fields as field}
								<div style="display: flex; gap: 12px; align-items: flex-start;">
									<dt style="font-size: 12px; color: var(--color-text-muted); min-width: 140px; flex-shrink: 0; padding-top: 1px;">{field.label}</dt>
									<dd style="font-size: 13px; color: var(--color-text); margin: 0; line-height: 1.4;">{field.value}</dd>
								</div>
							{/each}
						</dl>
					</section>
				{/if}

				{#if missing.length > 0 || flags.length > 0}
					<div style="display: flex; flex-direction: column; gap: 12px;">
						{#if missing.length > 0}
							<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-urgency-medium); border-radius: 8px; padding: 14px 16px;">
								<div style="font-size: 11px; color: var(--color-urgency-medium); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">Missing Information</div>
								<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px;">
									{#each missing as f}
										<li style="font-size: 13px; color: var(--color-text); display: flex; gap: 8px; align-items: flex-start;">
											<span style="color: var(--color-urgency-medium); margin-top: 1px; flex-shrink: 0;">!</span>{f}
										</li>
									{/each}
								</ul>
							</section>
						{/if}
						{#if flags.length > 0}
							<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-urgency-high); border-radius: 8px; padding: 14px 16px;">
								<div style="font-size: 11px; color: var(--color-urgency-high); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;">Risk Flags</div>
								<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px;">
									{#each flags as flag}
										<li style="font-size: 13px; color: var(--color-text); display: flex; gap: 8px; align-items: flex-start;">
											<span style="color: var(--color-urgency-high); margin-top: 1px; flex-shrink: 0;">▲</span>{flag}
										</li>
									{/each}
								</ul>
							</section>
						{/if}
					</div>
				{/if}
			</div>
			<!-- Contract Terms Panel -->
			{#if selected.analysis}
				<ContractTermsPanel
					docType={selected.type}
					analyzerOutputs={selected.analysis.analyzer_outputs}
				/>
			{/if}

			<!-- Draft Reply Panel (client_request only) -->
			{#if selected.type === 'client_request' && selected.analysis}
				<DraftReplyPanel analyzerOutputs={selected.analysis.analyzer_outputs} />
			{/if}
		{:else if selected.status === 'done'}
			<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px; margin-bottom: 16px;">
				<p style="font-size: 14px; color: var(--color-text-muted); margin: 0;">
					Analysis complete — no supported analyzer for this document type.
				</p>
			</section>
		{:else if selected.status === 'failed'}
			<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-urgency-high); border-radius: 8px; padding: 18px 20px; margin-bottom: 16px;">
				<p style="font-size: 14px; color: var(--color-urgency-high); margin: 0;">
					Analysis failed. Check the audit log for details.
				</p>
			</section>
		{/if}

		<!-- Human Approval -->
		{#if selected}
			{@const isApproved = localApproved.has(selected.id) || selected.audit_events.some((e) => e.event_type === 'approved')}
			<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
				<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">Human Approval</div>
				<p style="font-size: 13px; color: var(--color-text-muted); margin: 0 0 14px; line-height: 1.5;">
					AI has prepared the analysis above. Review it and decide the next step.
				</p>
				<div style="display: flex; gap: 10px; flex-wrap: wrap;">
					<button
						onclick={() => approveDoc(selected!.id)}
						disabled={isApproved}
						style="background: {isApproved ? 'var(--color-urgency-low)' : 'var(--color-action)'}; color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 9px 20px; border-radius: 5px; font-size: 13px; cursor: {isApproved ? 'default' : 'pointer'}; font-weight: 500;"
					>
						{isApproved ? '✓ Approved' : 'Approve'}
					</button>
				</div>
			</section>
		{/if}

		<!-- Audit timeline -->
		<section style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
			<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">Audit Timeline</div>
			<div style="display: flex; flex-direction: column; gap: 0;">
				{#if selected.audit_events.length === 0}
					<div style="font-size: 13px; color: var(--color-text-muted);">No audit events yet.</div>
				{:else}
					{#each selected.audit_events as event, i}
						<div style="display: flex; gap: 14px; align-items: flex-start; padding: 8px 0; {i < selected.audit_events.length - 1 ? 'border-bottom: 1px solid var(--color-stroke);' : ''}">
							<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: {event.event_type === 'approved' ? 'var(--color-urgency-low)' : event.event_type.startsWith('analysis_failed') ? 'var(--color-urgency-high)' : 'var(--color-stroke-light)'}; margin-top: 5px;"></div>
							<div>
								<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 2px; font-family: monospace;">{fmtDate(event.created_at)}</div>
								<div style="font-size: 13px; color: var(--color-text);">{eventLabel(event.event_type)}</div>
							</div>
						</div>
					{/each}
				{/if}
			</div>
		</section>
	{/if}
</main>
