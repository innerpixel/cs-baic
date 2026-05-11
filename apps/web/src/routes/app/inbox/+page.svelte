<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { api, pdfUrl, type ApiDocumentDetail, type ApiDocumentItem } from '$lib/api/client.js';
	import ClassifierBadge from '$lib/components/ClassifierBadge.svelte';
	import ContractTermsPanel from '$lib/components/ContractTermsPanel.svelte';
	import DraftReplyPanel from '$lib/components/DraftReplyPanel.svelte';
	import PdfViewer from '$lib/components/PdfViewer.svelte';
	import ReviewActions from '$lib/components/ReviewActions.svelte';

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
	let uploading = $state(false);
	let uploadError = $state<string | null>(null);
	let fileInputEl = $state<HTMLInputElement | null>(null);

	// PDF tab state
	let showPdf = $state(false);

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

	const EVENT_LABELS: Record<string, string> = {
		uploaded: 'Document uploaded',
		approved: 'Approved by user',
		ocr_required: 'OCR required (image-only PDF)',
		not_supported_yet: 'Document type not yet supported'
	};

	const ANALYZER_LABELS: Record<string, string> = {
		invoice_extractor: 'Invoice extractor',
		classifier: 'Classifier',
		summarizer: 'Summarizer',
		contract_reviewer: 'Contract reviewer',
		document_indexer: 'Document indexer',
		draft_reply_generator: 'Draft reply'
	};

	function eventLabel(event_type: string): string {
		if (EVENT_LABELS[event_type]) return EVENT_LABELS[event_type];
		const colon = event_type.indexOf(':');
		if (colon !== -1) {
			const prefix = event_type.slice(0, colon);
			const suffix = event_type.slice(colon + 1);
			const suffixLabel = ANALYZER_LABELS[suffix] ?? suffix.replace(/_/g, ' ');
			if (prefix === 'analyzed_by') return `AI analysis · ${suffixLabel}`;
			if (prefix === 'analysis_failed') return `Analysis failed · ${suffixLabel}`;
			if (prefix === 'pipeline_failed') return `Pipeline error · ${suffixLabel}`;
			if (prefix === 'review_state_changed') return `Review state changed · ${suffix.replace('→', ' → ')}`;
		}
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
			// check for ?focus= param
			const focusId = $page.url.searchParams.get('focus');
			if (focusId && docs.some((d) => d.id === focusId)) {
				await selectDoc(focusId);
			} else if (!selectedId && docs.length > 0) {
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
		showPdf = false;
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
		if (!uploadFile) return;
		uploading = true;
		uploadError = null;
		try {
			const displayName = uploadFile.name;
			const result = await api.uploadFile(uploadFile);
			uploadFile = null;
			if (fileInputEl) fileInputEl.value = '';

			if (result.batch) {
				// ZIP: reload list to show all ingested docs
				await loadList();
			} else {
				docs = [
					{
						id: result.id,
						filename: displayName ?? result.id,
						type: 'unknown',
						source: 'public',
						review_state: 'pending',
						status: 'queued',
						created_at: new Date().toISOString()
					},
					...docs
				];
				await selectDoc(result.id);
				pollDoc(result.id);
			}
		} catch (e) {
			uploadError = String(e);
		} finally {
			uploading = false;
		}
	}

	async function handleReview(state: string, note?: string) {
		if (!selected) return;
		try {
			const result = await api.reviewState(selected.id, state, note);
			selected = { ...selected, review_state: result.review_state, review_note: result.review_note };
			docs = docs.map((d) => d.id === selected!.id ? { ...d, review_state: result.review_state } : d);
		} catch (e) {
			console.error('Review state update failed:', e);
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
				accept=".pdf,.zip,application/pdf,application/zip"
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
						Drop a PDF or ZIP<br />
						<span style="font-size: 11px;">or click to browse · max 5 MB PDF / 10 MB ZIP</span>
					</div>
				{/if}
			</div>

			<button
				type="submit"
				disabled={uploading || !uploadFile}
				style="background: var(--color-action); color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 8px; border-radius: 4px; font-size: 12px; cursor: pointer; font-weight: 500; opacity: {uploading || !uploadFile ? 0.5 : 1};"
			>
				{uploading ? 'Uploading…' : 'Upload'}
			</button>

			{#if uploadError}
				<div style="font-size: 11px; color: var(--color-urgency-high); line-height: 1.4;">
					{uploadError}
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
					<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
						<span style="font-size: 12px; color: {statusColor(doc.status)};">{doc.status}</span>
						{#if doc.review_state && doc.review_state !== 'pending'}
							<span style="font-size: 10px; padding: 1px 5px; border-radius: 2px; font-weight: 600; background: var(--color-data); border: 1px solid var(--color-stroke); color: {doc.review_state === 'approved' ? 'var(--color-urgency-low)' : doc.review_state === 'rejected' ? 'var(--color-urgency-high)' : '#d97706'};">
								{doc.review_state}
							</span>
						{/if}
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

		<!-- PDF Viewer (when available) -->
		{#if selected.pdf_path}
			<div style="margin-bottom: 16px;">
				<div style="display: flex; gap: 0; margin-bottom: 8px; border-bottom: 1px solid var(--color-stroke);">
					<button
						onclick={() => showPdf = false}
						style="background: none; border: none; border-bottom: 2px solid {!showPdf ? 'var(--color-stroke-light)' : 'transparent'}; color: {!showPdf ? 'var(--color-text)' : 'var(--color-text-muted)'}; font-size: 12px; padding: 6px 14px; cursor: pointer; font-family: inherit;"
					>
						AI Extraction
					</button>
					<button
						onclick={() => showPdf = true}
						style="background: none; border: none; border-bottom: 2px solid {showPdf ? 'var(--color-stroke-light)' : 'transparent'}; color: {showPdf ? 'var(--color-text)' : 'var(--color-text-muted)'}; font-size: 12px; padding: 6px 14px; cursor: pointer; font-family: inherit;"
					>
						Source PDF
					</button>
				</div>
				{#if showPdf}
					<PdfViewer pdfUrl={pdfUrl(selected.id)} />
				{/if}
			</div>
		{/if}

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

			<!-- Draft Reply Panel (client_request + accountant_request) -->
			{#if (selected.type === 'client_request' || selected.type === 'accountant_request') && selected.analysis}
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

		<!-- Human Review -->
		{#if selected}
			<section style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
				<div style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;">Human Review</div>
				<p style="font-size: 13px; color: var(--color-text-muted); margin: 0 0 14px; line-height: 1.5;">
					AI has prepared the analysis above. Review it and decide the next step.
				</p>
				<ReviewActions
					currentState={selected.review_state}
					onReview={handleReview}
				/>
				{#if selected.review_note}
					<div style="margin-top: 10px; font-size: 12px; color: var(--color-text-muted); background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 8px 10px; line-height: 1.5;">
						Note: {selected.review_note}
					</div>
				{/if}
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
