<script lang="ts">
	let { children } = $props();
</script>

<!-- App shell: top bar + content area -->
<div style="min-height: 100vh; display: flex; flex-direction: column;">
	<nav style="background: var(--color-data); border-bottom: 1px solid var(--color-stroke); flex-shrink: 0;">
		<div
			style="max-width: 1400px; margin: 0 auto; padding: 0 20px; height: 52px; display: flex; align-items: center; justify-content: space-between;"
		>
			<div style="display: flex; align-items: center; gap: 20px;">
				<a href="/" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">
					← Business Companion AI
				</a>
				<span style="color: var(--color-stroke); font-size: 13px;">|</span>
				<span style="color: var(--color-text); font-size: 13px; font-weight: 500;">Atelier Nova SRL</span>
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
