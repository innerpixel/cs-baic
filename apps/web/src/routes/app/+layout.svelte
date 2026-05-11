<script lang="ts">
	import { page } from '$app/stores';
	let { children } = $props();

	const navItems = [
		{ href: '/app/inbox', label: 'AI Inbox' },
		{ href: '/app/ask', label: 'Ask My Company' }
	];
</script>

<!-- App shell: top bar + sidebar nav + content area -->
<div style="min-height: 100vh; display: flex; flex-direction: column;">
	<nav style="background: var(--color-data); border-bottom: 1px solid var(--color-stroke); flex-shrink: 0;">
		<div
			style="max-width: 1400px; margin: 0 auto; padding: 0 20px; height: 52px; display: flex; align-items: center; justify-content: space-between;"
		>
			<div style="display: flex; align-items: center; gap: 20px;">
				<a href="/" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">
					← NovAI Desk
				</a>
				<span style="color: var(--color-stroke); font-size: 13px;">|</span>
				<span style="color: var(--color-text); font-size: 13px; font-weight: 500;">Atelier Nova SRL</span>
				<span style="color: var(--color-stroke); font-size: 13px;">|</span>
				<div style="display: flex; align-items: center; gap: 4px;">
					{#each navItems as item}
						<a
							href={item.href}
							style="font-size: 13px; text-decoration: none; padding: 5px 12px; border-radius: 4px; background: {$page.url.pathname.startsWith(item.href) ? 'var(--color-action)' : 'transparent'}; color: {$page.url.pathname.startsWith(item.href) ? 'var(--color-text)' : 'var(--color-text-muted)'}; border: 1px solid {$page.url.pathname.startsWith(item.href) ? 'var(--color-stroke)' : 'transparent'};"
						>
							{item.label}
						</a>
					{/each}
				</div>
			</div>
			<div style="font-size: 12px; color: var(--color-text-muted);">
				Demo workspace · All data synthetic
			</div>
		</div>
	</nav>
	<div style="flex: 1; display: flex; overflow: hidden;">
		{@render children()}
	</div>
</div>
