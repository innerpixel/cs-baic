<script lang="ts">
	import { matchQuestion, EXAMPLE_QUESTIONS, type QAResult } from '$lib/data/qa.js';

	interface Message {
		role: 'user' | 'assistant';
		text: string;
		sources?: string[];
		fallback?: boolean;
	}

	let messages = $state<Message[]>([]);
	let inputValue = $state('');
	let listEl = $state<HTMLElement | null>(null);

	function scrollToBottom() {
		if (listEl) listEl.scrollTop = listEl.scrollHeight;
	}

	function submit() {
		const q = inputValue.trim();
		if (!q) return;
		inputValue = '';

		messages = [...messages, { role: 'user', text: q }];

		const result: QAResult | null = matchQuestion(q);
		if (result) {
			messages = [
				...messages,
				{ role: 'assistant', text: result.answer, sources: result.sources }
			];
		} else {
			messages = [
				...messages,
				{
					role: 'assistant',
					text: 'Information not found in your documents.',
					fallback: true
				}
			];
		}

		setTimeout(scrollToBottom, 0);
	}

	function useExample(q: string) {
		inputValue = q;
		submit();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			submit();
		}
	}
</script>

<svelte:head>
	<title>Ask My Company — Atelier Nova SRL — Business Companion AI</title>
</svelte:head>

<!-- Sidebar -->
<aside
	style="width: 260px; flex-shrink: 0; background: var(--color-data); border-right: 1px solid var(--color-stroke); overflow-y: auto; display: flex; flex-direction: column;"
>
	<div style="padding: 16px 16px 12px; border-bottom: 1px solid var(--color-stroke);">
		<div
			style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 2px;"
		>
			Ask My Company
		</div>
		<div style="font-size: 13px; color: var(--color-stroke-light);">
			Answers from your documents
		</div>
	</div>

	<div style="padding: 14px 16px; flex: 1;">
		<div
			style="font-size: 11px; color: var(--color-text-muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 10px;"
		>
			Example questions
		</div>
		<div style="display: flex; flex-direction: column; gap: 6px;">
			{#each EXAMPLE_QUESTIONS as q}
				<button
					onclick={() => useExample(q)}
					style="text-align: left; background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 5px; padding: 8px 11px; font-size: 12px; color: var(--color-text-muted); cursor: pointer; line-height: 1.4; transition: border-color 0.15s;"
				>
					{q}
				</button>
			{/each}
		</div>
	</div>

	<div style="padding: 12px 16px; border-top: 1px solid var(--color-stroke);">
		<a
			href="/demo"
			style="font-size: 12px; color: var(--color-text-muted); text-decoration: none;"
			>← Back to demo workflow</a
		>
	</div>
</aside>

<!-- Main chat area -->
<main style="flex: 1; display: flex; flex-direction: column; overflow: hidden; max-width: 820px;">
	<!-- Message list -->
	<div
		bind:this={listEl}
		style="flex: 1; overflow-y: auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 16px;"
	>
		{#if messages.length === 0}
			<div
				style="margin: auto; text-align: center; max-width: 400px; padding: 40px 0;"
			>
				<div
					style="font-size: 14px; color: var(--color-text-muted); line-height: 1.7; margin-bottom: 10px;"
				>
					Ask a question about your documents.<br />Only information from your uploaded files will be used.
				</div>
				<div style="font-size: 12px; color: var(--color-stroke);">
					Try an example question from the sidebar.
				</div>
			</div>
		{/if}

		{#each messages as msg}
			{#if msg.role === 'user'}
				<div style="display: flex; justify-content: flex-end;">
					<div
						style="background: var(--color-action); border: 1px solid var(--color-stroke-light); border-radius: 8px 8px 2px 8px; padding: 12px 16px; max-width: 75%; font-size: 14px; color: var(--color-text); line-height: 1.5;"
					>
						{msg.text}
					</div>
				</div>
			{:else}
				<div style="display: flex; justify-content: flex-start;">
					<div style="max-width: 85%;">
						<div
							style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 2px 8px 8px 8px; padding: 14px 18px; font-size: 14px; color: var(--color-text); line-height: 1.65;"
						>
							{#if msg.fallback}
								<div>
									<span style="color: var(--color-text-muted);">Information not found in your documents.</span>
								</div>
								<div style="margin-top: 10px; font-size: 12px; color: var(--color-stroke);">
									Try one of the 8 example questions, or upload more documents to expand what can be answered.
								</div>
							{:else}
								{@html msg.text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}
							{/if}
						</div>

						{#if msg.sources && msg.sources.length > 0}
							<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; padding-left: 2px;">
								{#each msg.sources as src}
									<a
										href="/app/inbox"
										style="font-size: 11px; font-family: monospace; background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 3px; padding: 2px 8px; color: var(--color-text-muted); text-decoration: none; white-space: nowrap;"
									>
										{src}
									</a>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			{/if}
		{/each}
	</div>

	<!-- Input bar -->
	<div
		style="flex-shrink: 0; border-top: 1px solid var(--color-stroke); background: var(--color-data); padding: 16px 20px; display: flex; gap: 10px; align-items: flex-end;"
	>
		<textarea
			bind:value={inputValue}
			onkeydown={handleKeydown}
			rows={2}
			placeholder="Ask a question about your documents…"
			style="flex: 1; background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 10px 14px; font-size: 14px; color: var(--color-text); resize: none; font-family: inherit; line-height: 1.5; outline: none;"
		></textarea>
		<button
			onclick={submit}
			style="background: var(--color-action); border: 1px solid var(--color-stroke-light); color: var(--color-text); padding: 10px 18px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; flex-shrink: 0;"
		>
			Ask
		</button>
	</div>
</main>
