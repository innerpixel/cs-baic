<script lang="ts">
	interface ContractOutput {
		payment_terms?: string[];
		penalties?: string[];
		termination_terms?: string[];
		questions_for_human_review?: string[];
		plain_language_summary?: string;
		recommended_next_action?: string;
		risk_flags?: string[];
		parties?: string[];
		start_date?: string | null;
		end_date?: string | null;
	}

	interface Props {
		docType: string;
		analyzerOutputs: Record<string, unknown> | null;
	}
	let { docType, analyzerOutputs }: Props = $props();

	const isContract = $derived(
		docType === 'contract' || docType === 'Contract' || docType === 'Supplier Contract'
	);
	const review = $derived<ContractOutput | null>(
		isContract && analyzerOutputs?.['contract_reviewer']
			? (analyzerOutputs['contract_reviewer'] as ContractOutput)
			: null
	);

	let open = $state(true);
</script>

{#if review}
	<section
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-stroke-light); border-radius: 8px; margin-bottom: 16px; overflow: hidden;"
	>
		<button
			onclick={() => (open = !open)}
			style="width: 100%; text-align: left; background: none; border: none; padding: 14px 20px; cursor: pointer; display: flex; justify-content: space-between; align-items: center;"
		>
			<span style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase;">
				Contract Terms
			</span>
			<span style="font-size: 12px; color: var(--color-text-muted);">{open ? '▲' : '▼'}</span>
		</button>

		{#if open}
			<div style="padding: 0 20px 16px; display: flex; flex-direction: column; gap: 12px;">
				{#if review.plain_language_summary}
					<p style="font-size: 13px; color: var(--color-text); line-height: 1.6; margin: 0;">
						{review.plain_language_summary}
					</p>
				{/if}

				{#if review.payment_terms && review.payment_terms.length > 0}
					<div>
						<div style="font-size: 11px; color: var(--color-text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">Payment Terms</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px;">
							{#each review.payment_terms as term}
								<li style="font-size: 13px; color: var(--color-text);">· {term}</li>
							{/each}
						</ul>
					</div>
				{/if}

				{#if review.penalties && review.penalties.length > 0}
					<div>
						<div style="font-size: 11px; color: var(--color-urgency-high); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">Penalties</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px;">
							{#each review.penalties as p}
								<li style="font-size: 13px; color: var(--color-text);">· {p}</li>
							{/each}
						</ul>
					</div>
				{/if}

				{#if review.termination_terms && review.termination_terms.length > 0}
					<div>
						<div style="font-size: 11px; color: var(--color-text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">Termination</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px;">
							{#each review.termination_terms as t}
								<li style="font-size: 13px; color: var(--color-text);">· {t}</li>
							{/each}
						</ul>
					</div>
				{/if}

				{#if review.questions_for_human_review && review.questions_for_human_review.length > 0}
					<div style="background: var(--color-data); border: 1px solid var(--color-stroke); border-left: 3px solid var(--color-urgency-medium); border-radius: 4px; padding: 10px 12px;">
						<div style="font-size: 11px; color: var(--color-urgency-medium); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em;">Questions for Human Review</div>
						<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px;">
							{#each review.questions_for_human_review as q}
								<li style="font-size: 13px; color: var(--color-text);">? {q}</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		{/if}
	</section>
{/if}
