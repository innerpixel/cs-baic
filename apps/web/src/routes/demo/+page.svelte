<script lang="ts">
	import { browser } from '$app/environment';

	const API_BASE = browser
		? (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')
		: 'http://localhost:8000';

	const archiveUrl = `${API_BASE}/api/demo/atelier-nova/archive.zip`;

	const steps = [
		{
			number: '01',
			title: 'Documentele sosesc',
			description:
				'Atelier Nova SRL primește facturi de la furnizori (Lumina Design, Mobilier Concept), cereri de la contabil (Bilanț Clar SRL), emailuri de la clienți (Dr. Popa, Aurora Construct) și contracte cu furnizorii — prin canale diferite.',
			detail: 'Facturi · Contracte · Oferte · Cereri de la clienți · Cereri de la contabil',
			accent: false
		},
		{
			number: '02',
			title: 'AI creează carduri în Inbox',
			description:
				'Fiecare document este clasificat automat: tip, limbă, urgență. Inbox-ul organizează totul în carduri structurate, gata de verificat.',
			detail: 'Factură furnizor · Cerere contabil · Cerere client · Contract furnizor · Ofertă',
			accent: false
		},
		{
			number: '03',
			title: 'AI extrage datele cheie',
			description:
				'Pentru facturi: furnizor, sumă, scadență, IBAN. Pentru contracte: termene de plată, penalități, durată. Pentru emailuri: cererea principală, datele lipsă, urgența.',
			detail: 'Sume · Scadențe · Părți contractante · Obligații · Câmpuri lipsă',
			accent: false
		},
		{
			number: '04',
			title: 'AI semnalează informațiile lipsă',
			description:
				'Unele documente vin incomplete. AI-ul marchează exact ce lipsește: un număr de comandă intern, un brief de la client, documentele solicitate de contabil.',
			detail: 'Câmpuri lipsă vizibile pe fiecare card',
			accent: true
		},
		{
			number: '05',
			title: 'AI sugerează acțiunea următoare',
			description:
				'Pentru fiecare document: o acțiune concretă sugerată. Solicită numărul de comandă lipsă. Adună cele patru documente pentru contabil. Răspunde clientului cu o cerere de brief.',
			detail: 'Acțiune sugerată vizibilă pe fiecare card',
			accent: false
		},
		{
			number: '06',
			title: 'Tu verifici și aprobi',
			description:
				'Deschizi fiecare card, citești rezumatul AI, verifici câmpurile extrase și decizi: aprobat, necesită verificare sau respins. Nimic nu se trimite automat.',
			detail: 'Aprobat · Necesită verificare · Respins — nicio decizie autonomă',
			accent: false
		},
		{
			number: '07',
			title: 'Acțiunea e înregistrată în jurnal',
			description:
				'Fiecare decizie este salvată: ce a sugerat AI-ul, ce ai aprobat tu și când. Documentul trece în starea corectă: verificat, aprobat sau în așteptare.',
			detail: 'Jurnal de audit complet · Referințe la surse · Marker de aprobare umană',
			accent: false
		}
	];

	const inboxCards = [
		{
			filename: 'factura_lumina_design_2026_0041.pdf',
			type: 'Factură furnizor',
			urgency: 'Ridicată',
			urgencyColor: 'var(--color-urgency-high)',
			summary: 'Panouri LED și accesorii — 3.046,40 RON — scadent 12.05.2026',
			flag: 'Număr comandă lipsă'
		},
		{
			filename: 'email_contabil_documente_aprilie.pdf',
			type: 'Cerere contabil',
			urgency: 'Ridicată',
			urgencyColor: 'var(--color-urgency-high)',
			summary: '4 documente solicitate de Mihai — termen 10 mai',
			flag: 'Termen în 5 zile'
		},
		{
			filename: 'cerere_client_dr_popa_remodelare.pdf',
			type: 'Cerere client',
			urgency: 'Medie',
			urgencyColor: 'var(--color-urgency-medium)',
			summary: 'Remodelare cabinet medical 65 mp — ofertă solicitată',
			flag: 'Brief incomplet'
		},
		{
			filename: 'contract_mobilier_concept_colaborare.pdf',
			type: 'Contract furnizor',
			urgency: 'Scăzută',
			urgencyColor: 'var(--color-urgency-low)',
			summary: 'Contract colaborare — valabil până 31.12.2026 — 2 clauze de risc',
			flag: 'Clauze penalități'
		}
	];
</script>

<svelte:head>
	<title>Demo — NovAI Desk</title>
	<meta
		name="description"
		content="Vezi cum NovAI Desk procesează facturi, emailuri, contracte și cereri de la contabil pentru o firmă românească de design interior."
	/>
</svelte:head>

<!-- NAV -->
<nav style="background: var(--color-data); border-bottom: 1px solid var(--color-stroke);">
	<div
		style="max-width: 1100px; margin: 0 auto; padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between;"
	>
		<a href="/" style="color: var(--color-text); text-decoration: none; font-weight: 600; font-size: 15px;">
			NovAI Desk
		</a>
		<div style="display: flex; gap: 24px; align-items: center;">
			<a href="/" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">Acasă</a>
			<a href="/about" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">Despre</a>
			<a href="/demo" style="color: var(--color-text); text-decoration: none; font-size: 14px; font-weight: 500;">Demo</a>
			<a
				href="/app/inbox"
				style="background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 7px 16px; border-radius: 5px; font-size: 13px; border: 1px solid var(--color-stroke);"
			>
				Aplicație
			</a>
		</div>
	</div>
</nav>

<!-- HEADER -->
<section style="max-width: 1100px; margin: 0 auto; padding: 56px 24px 40px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Demo · Atelier Nova SRL
	</p>
	<h1 style="font-size: clamp(24px, 4vw, 36px); font-weight: 700; color: var(--color-text); margin: 0 0 16px; max-width: 640px; line-height: 1.25;">
		De la documente disparate la acțiuni clare
	</h1>
	<p style="color: var(--color-text-muted); font-size: 16px; line-height: 1.6; max-width: 600px; margin: 0 0 32px;">
		O firmă de design interior din Pitești primește facturi, cereri de la clienți și emailuri de la
		contabil. NovAI Desk citește totul, clasifică, extrage câmpurile importante și arată ce
		necesită aprobare umană.
	</p>

	<!-- TWO CTAs -->
	<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 32px;">
		<a
			href={archiveUrl}
			download
			style="display: inline-flex; align-items: center; gap: 8px; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 11px 22px; border-radius: 6px; font-size: 14px; font-weight: 500; border: 1px solid var(--color-stroke-light);"
		>
			Descarcă arhiva demo
		</a>
		<a
			href="/app/inbox"
			style="display: inline-flex; align-items: center; gap: 8px; background: transparent; color: var(--color-text); text-decoration: none; padding: 11px 22px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke);"
		>
			Deschide aplicația →
		</a>
	</div>

	<div
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 18px; display: inline-flex; gap: 24px; font-size: 13px; color: var(--color-text-muted); flex-wrap: wrap;"
	>
		<span>Compania demo: <strong style="color: var(--color-text);">Atelier Nova SRL</strong></span>
		<span>18 documente procesate</span>
		<span>Toate datele sunt sintetice</span>
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- WORKFLOW STEPS -->
<section style="max-width: 1100px; margin: 0 auto; padding: 48px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 24px;">
		Fluxul de lucru
	</p>
	<div style="display: flex; flex-direction: column; gap: 4px;">
		{#each steps as step, i}
			<div
				style="display: flex; gap: 24px; padding: 24px 0; border-bottom: 1px solid var(--color-stroke); {i === 0
					? 'border-top: 1px solid var(--color-stroke);' : ''}"
			>
				<div
					style="flex-shrink: 0; width: 48px; height: 48px; background: {step.accent
						? 'var(--color-action)'
						: 'var(--color-main)'}; border: 1px solid var(--color-stroke); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; color: var(--color-text-muted); margin-top: 2px;"
				>
					{step.number}
				</div>
				<div style="flex: 1;">
					<h3 style="font-size: 16px; font-weight: 600; color: var(--color-text); margin: 0 0 8px;">
						{step.title}
					</h3>
					<p style="font-size: 14px; color: var(--color-text-muted); line-height: 1.6; margin: 0 0 10px; max-width: 640px;">
						{step.description}
					</p>
					<div
						style="font-size: 12px; color: var(--color-stroke-light); background: var(--color-data); border-radius: 4px; padding: 4px 10px; display: inline-block;"
					>
						{step.detail}
					</div>
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- MOCK INBOX CARDS PREVIEW -->
<section
	style="background: var(--color-main); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 48px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
			Inbox-ul după procesare
		</p>
		<p style="color: var(--color-text-muted); font-size: 13px; margin-bottom: 28px;">
			Câteva exemple din cardurile generate pentru Atelier Nova SRL. Deschide aplicația pentru a le explora pe toate.
		</p>
		<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 28px;">
			{#each inboxCards as card}
				<div
					style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 16px 18px;"
				>
					<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
						<span
							style="font-size: 11px; background: var(--color-action); color: var(--color-text-muted); padding: 2px 8px; border-radius: 3px;"
						>
							{card.type}
						</span>
						<span
							style="font-size: 11px; color: {card.urgencyColor}; font-weight: 600;"
						>
							{card.urgency}
						</span>
					</div>
					<div style="font-size: 12px; color: var(--color-stroke-light); margin-bottom: 6px; font-family: monospace;">
						{card.filename}
					</div>
					<div style="font-size: 13px; color: var(--color-text); line-height: 1.5; margin-bottom: 10px;">
						{card.summary}
					</div>
					<div
						style="font-size: 11px; color: var(--color-urgency-medium); background: var(--color-data); padding: 3px 8px; border-radius: 3px; display: inline-block;"
					>
						{card.flag}
					</div>
				</div>
			{/each}
		</div>
		<div style="display: flex; gap: 12px; flex-wrap: wrap;">
			<a
				href="/app/inbox"
				style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 11px 22px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke-light);"
			>
				Deschide aplicația →
			</a>
			<a
				href={archiveUrl}
				download
				style="display: inline-block; background: transparent; color: var(--color-text); text-decoration: none; padding: 11px 22px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke);"
			>
				Descarcă arhiva demo
			</a>
		</div>
	</div>
</section>

<!-- NOTA DATE SINTETICE -->
<section style="max-width: 1100px; margin: 0 auto; padding: 40px 24px;">
	<p style="font-size: 13px; color: var(--color-text-muted); line-height: 1.7; max-width: 640px;">
		Toate documentele din arhivă sunt <strong style="color: var(--color-text);">sintetice</strong> — generate special pentru acest demo.
		Câmpurile sensibile (CUI, IBAN, telefon, J-number) conțin caracterul
		<code style="background: var(--color-data); padding: 1px 5px; border-radius: 3px; font-size: 12px;">Ɛ</code>
		pentru a preveni orice confuzie cu date reale.
		<a href="/about" style="color: var(--color-stroke-light); text-decoration: underline;">Află mai multe despre proiect</a>.
	</p>
</section>

<!-- FOOTER -->
<footer style="max-width: 1100px; margin: 0 auto; padding: 32px 24px; border-top: 1px solid var(--color-stroke);">
	<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
		<div style="font-size: 13px; color: var(--color-text-muted);">NovAI Desk · demo</div>
		<div style="display: flex; gap: 20px; align-items: center;">
			<a href="/" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Acasă</a>
			<a href="/about" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Despre</a>
			<a href="/app/inbox" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Aplicație</a>
		</div>
	</div>
</footer>
