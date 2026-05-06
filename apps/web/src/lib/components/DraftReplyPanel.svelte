<script lang="ts">
	interface Props {
		analyzerOutputs: Record<string, unknown> | null;
	}

	let { analyzerOutputs }: Props = $props();

	const draft = $derived(
		analyzerOutputs?.draft_reply_generator as
			| {
					detected_language?: string;
					reply_subject?: string;
					reply_body?: string;
					assumptions?: string[];
					missing_information?: string[];
					human_review_required?: boolean;
					recommended_next_action?: string | null;
			  }
			| undefined
	);

	let expanded = $state(true);
</script>

{#if draft && (draft.reply_body || draft.reply_subject)}
	<section
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-top: 2px solid var(--color-stroke-light); border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;"
	>
		<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
			<div
				style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; flex: 1;"
			>
				Draft Reply
			</div>
			<span
				style="font-size: 10px; color: var(--color-urgency-low); background: var(--color-data); border: 1px solid var(--color-stroke); padding: 1px 7px; border-radius: 3px; font-weight: 600; letter-spacing: 0.05em;"
			>
				LIVE
			</span>
			{#if draft.detected_language}
				<span
					style="font-size: 10px; color: var(--color-text-muted); background: var(--color-data); border: 1px solid var(--color-stroke); padding: 1px 7px; border-radius: 3px; font-family: monospace;"
				>
					{draft.detected_language}
				</span>
			{/if}
			<button
				onclick={() => (expanded = !expanded)}
				style="font-size: 12px; color: var(--color-text-muted); background: none; border: none; cursor: pointer; padding: 0 4px;"
			>
				{expanded ? '▲' : '▼'}
			</button>
		</div>

		{#if expanded}
			{#if draft.reply_subject}
				<div style="margin-bottom: 10px;">
					<div
						style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px;"
					>
						Subject
					</div>
					<div
						style="font-size: 13px; color: var(--color-text); background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 8px 12px;"
					>
						{draft.reply_subject}
					</div>
				</div>
			{/if}

			{#if draft.reply_body}
				<div style="margin-bottom: 14px;">
					<div
						style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px;"
					>
						Draft Body
					</div>
					<div
						style="font-size: 13px; color: var(--color-text); background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 12px 14px; white-space: pre-wrap; line-height: 1.65; font-family: inherit;"
					>
						{draft.reply_body}
					</div>
				</div>
			{/if}

			{#if draft.missing_information && draft.missing_information.length > 0}
				<div style="margin-bottom: 12px;">
					<div
						style="font-size: 11px; color: var(--color-urgency-medium); letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 6px;"
					>
						Before Sending — Information Needed
					</div>
					<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 5px;">
						{#each draft.missing_information as item}
							<li
								style="font-size: 13px; color: var(--color-text); display: flex; gap: 8px; align-items: flex-start;"
							>
								<span style="color: var(--color-urgency-medium); flex-shrink: 0; margin-top: 1px;">!</span
								>{typeof item === 'string' ? item : JSON.stringify(item)}
							</li>
						{/each}
					</ul>
				</div>
			{/if}

			{#if draft.recommended_next_action}
				<div
					style="font-size: 12px; color: var(--color-text-muted); background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 8px 12px; margin-bottom: 14px; line-height: 1.5;"
				>
					<strong>Next step:</strong>
					{draft.recommended_next_action}
				</div>
			{/if}

			<div
				style="display: flex; gap: 10px; padding-top: 4px; border-top: 1px solid var(--color-stroke);"
			>
				<div
					style="font-size: 12px; color: var(--color-urgency-medium); padding: 8px 0; flex: 1; line-height: 1.5;"
				>
					⚠ Human review required before sending. AI does not send emails.
				</div>
			</div>
		{/if}
	</section>
{/if}
