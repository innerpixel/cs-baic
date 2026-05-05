<script lang="ts">
	interface Props {
		detectedType: string | null;
		docType: string;
		confidence: number | null;
	}
	let { detectedType, docType, confidence }: Props = $props();

	// Normalize type strings for comparison (both may be "supplier_invoice" or similar)
	const normalize = (t: string) => t.toLowerCase().replace(/[\s-]/g, '_');

	const show = $derived(
		detectedType !== null &&
		confidence !== null &&
		confidence >= 0.6 &&
		normalize(detectedType) !== normalize(docType)
	);

	const pct = $derived(confidence !== null ? Math.round(confidence * 100) : 0);
	const label = $derived(detectedType?.replace(/_/g, ' ') ?? '');
</script>

{#if show}
	<span
		style="
			font-size: 11px;
			background: var(--color-data);
			border: 1px solid var(--color-stroke);
			border-left: 3px solid var(--color-urgency-medium);
			padding: 2px 8px;
			border-radius: 3px;
			color: var(--color-urgency-medium);
			white-space: nowrap;
		"
	>
		AI-classified as {label} ({pct}%)
	</span>
{/if}
