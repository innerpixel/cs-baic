<script lang="ts">
	let {
		currentState,
		onReview
	}: {
		currentState: string | null;
		onReview: (state: string, note?: string) => void;
	} = $props();

	let showNoteFor = $state<string | null>(null);
	let noteText = $state('');

	function stateColor(state: string | null) {
		if (state === 'approved') return 'var(--color-urgency-low)';
		if (state === 'needs_review') return '#d97706';
		if (state === 'rejected') return 'var(--color-urgency-high)';
		return 'var(--color-text-muted)';
	}

	function stateLabel(state: string | null) {
		if (state === 'approved') return 'Approved';
		if (state === 'needs_review') return 'Needs review';
		if (state === 'rejected') return 'Rejected';
		return 'Pending';
	}

	function handleClick(state: string) {
		if (state === 'needs_review' || state === 'rejected') {
			if (showNoteFor === state) {
				onReview(state, noteText.trim() || undefined);
				showNoteFor = null;
				noteText = '';
			} else {
				showNoteFor = state;
				noteText = '';
			}
		} else {
			showNoteFor = null;
			onReview(state);
		}
	}
</script>

<div>
	<div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 10px;">
		<div style="font-size: 11px; color: var(--color-text-muted); margin-right: 4px;">
			Status: <strong style="color: {stateColor(currentState)};">{stateLabel(currentState)}</strong>
		</div>
		<button
			onclick={() => handleClick('approved')}
			disabled={currentState === 'approved'}
			style="background: {currentState === 'approved' ? 'var(--color-urgency-low)' : 'var(--color-action)'}; color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 7px 16px; border-radius: 4px; font-size: 12px; cursor: {currentState === 'approved' ? 'default' : 'pointer'}; font-weight: 500;"
		>
			{currentState === 'approved' ? '✓ Approved' : 'Approve'}
		</button>
		<button
			onclick={() => handleClick('needs_review')}
			disabled={currentState === 'needs_review'}
			style="background: {currentState === 'needs_review' ? '#92400e' : 'var(--color-action)'}; color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 7px 16px; border-radius: 4px; font-size: 12px; cursor: {currentState === 'needs_review' ? 'default' : 'pointer'};"
		>
			{currentState === 'needs_review' ? '⚑ Needs review' : 'Mark needs review'}
		</button>
		<button
			onclick={() => handleClick('rejected')}
			disabled={currentState === 'rejected'}
			style="background: {currentState === 'rejected' ? 'var(--color-urgency-high)' : 'var(--color-action)'}; color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 7px 16px; border-radius: 4px; font-size: 12px; cursor: {currentState === 'rejected' ? 'default' : 'pointer'};"
		>
			{currentState === 'rejected' ? '✗ Rejected' : 'Reject'}
		</button>
	</div>

	{#if showNoteFor}
		<div style="display: flex; gap: 8px; align-items: flex-start;">
			<textarea
				bind:value={noteText}
				placeholder="Add a note (optional)…"
				rows={2}
				style="flex: 1; background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 4px; padding: 7px 10px; font-size: 12px; color: var(--color-text); font-family: inherit; resize: vertical; outline: none;"
			></textarea>
			<button
				onclick={() => handleClick(showNoteFor!)}
				style="background: var(--color-action); color: var(--color-text); border: 1px solid var(--color-stroke-light); padding: 7px 14px; border-radius: 4px; font-size: 12px; cursor: pointer; white-space: nowrap;"
			>
				Confirm
			</button>
			<button
				onclick={() => { showNoteFor = null; noteText = ''; }}
				style="background: none; color: var(--color-text-muted); border: 1px solid var(--color-stroke); padding: 7px 10px; border-radius: 4px; font-size: 12px; cursor: pointer;"
			>
				Cancel
			</button>
		</div>
	{/if}
</div>
