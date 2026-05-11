<script lang="ts">
	let { pdfUrl }: { pdfUrl: string } = $props();
</script>

<div style="width: 100%; border: 1px solid var(--color-stroke); border-radius: 6px; overflow: hidden; background: var(--color-data);">
	<object
		data={pdfUrl}
		type="application/pdf"
		title="Document PDF preview"
		style="width: 100%; height: 520px; display: block; border: none;"
	>
		<!-- fallback for browsers that block inline PDFs -->
		<div style="padding: 24px; text-align: center;">
			<p style="color: var(--color-text-muted); font-size: 13px; margin: 0 0 12px;">
				Your browser does not support inline PDF preview.
			</p>
			<a
				href={pdfUrl}
				target="_blank"
				rel="noopener"
				style="color: var(--color-stroke-light); font-size: 13px; text-decoration: underline;"
			>
				Open PDF in new tab →
			</a>
		</div>
	</object>
</div>
