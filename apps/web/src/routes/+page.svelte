<script lang="ts">
	const pains = [
		'Facturi cu scadențe uitate până e prea târziu',
		'Emailuri de la clienți care așteaptă zile întregi un răspuns',
		'Contabilul cere documente pe care nu le mai găsești repede',
		'Contracte cu clauze pe care le redescoperi abia când apare o problemă',
		'Cereri de ofertă pierdute printre emailuri',
		'Nicio imagine clară despre ce necesită atenție săptămâna aceasta'
	];
</script>

<svelte:head>
	<title>NovAI Desk — Inbox AI pentru firme românești</title>
	<meta
		name="description"
		content="NovAI Desk organizează automat facturile, emailurile, contractele și cererile contabilului tău într-un singur spațiu de lucru privat."
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
			<a href="/" style="color: var(--color-text); text-decoration: none; font-size: 14px; font-weight: 500;">Acasă</a>
			<a href="/about" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">Despre</a>
			<a href="/demo" style="color: var(--color-text-muted); text-decoration: none; font-size: 14px;">Demo</a>
			<a
				href="/app/inbox"
				style="background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 7px 16px; border-radius: 5px; font-size: 13px; border: 1px solid var(--color-stroke);"
			>
				Aplicație
			</a>
		</div>
	</div>
</nav>

<!-- HERO -->
<section style="max-width: 1100px; margin: 0 auto; padding: 80px 24px 64px;">
	<div style="max-width: 680px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px;">
			Pentru firme românești · Spațiu de lucru AI privat
		</p>
		<h1 style="font-size: clamp(28px, 5vw, 44px); font-weight: 700; line-height: 1.2; color: var(--color-text); margin: 0 0 20px;">
			AI care îți cunoaște compania și te ajută să gestionezi cererile și informațiile care îți intră zilnic în inbox.
		</h1>
		<p style="font-size: 17px; color: var(--color-text-muted); line-height: 1.6; margin: 0 0 36px;">
			Facturi, emailuri de la clienți, cereri de la contabil, contracte cu furnizori — toate clasificate,
			rezumate și pregătite pentru decizia ta.
		</p>
		<div style="display: flex; gap: 12px; flex-wrap: wrap;">
			<a
				href="/demo"
				style="background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke-light); font-weight: 500;"
			>
				Explorează demo-ul
			</a>
			<a
				href="/about"
				style="background: transparent; color: var(--color-text); text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 15px; border: 1px solid var(--color-stroke);"
			>
				Despre proiect
			</a>
		</div>
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- PROBLEM -->
<section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Problema
	</p>
	<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 32px; max-width: 560px;">
		Documentele și cererile se acumulează. Termenele se pierd. Contextul dispare.
	</h2>
	<ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
		{#each pains as pain}
			<li
				style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 16px; display: flex; gap: 10px; align-items: flex-start;"
			>
				<span style="color: var(--color-stroke-light); margin-top: 2px; flex-shrink: 0;">—</span>
				<span style="color: var(--color-text); font-size: 14px; line-height: 1.5;">{pain}</span>
			</li>
		{/each}
	</ul>
</section>

<!-- HOW IT WORKS -->
<section
	style="background: var(--color-main); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
			Cum funcționează
		</p>
		<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 12px;">
			Încarci documentul. AI-ul îl citește. Tu decizi.
		</h2>
		<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.6; max-width: 600px; margin: 0 0 40px;">
			Fiecare document primit devine un card structurat: tip, rezumat, câmpuri extrase, urgență și
			acțiunea sugerată. Tu verifici și aprobi — nicio acțiune automată fără confirmarea ta.
		</p>
		<div
			style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px;"
		>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Pasul 1</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">Încarci documentul</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Factură, email, contract sau cerere — PDF sau arhivă ZIP.
				</div>
			</div>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Pasul 2</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">AI creează un card în Inbox</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Clasificare, rezumat, câmpuri extrase, urgență și acțiunea sugerată.
				</div>
			</div>
			<div style="background: var(--color-bg); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 18px 20px;">
				<div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 6px;">Pasul 3</div>
				<div style="font-weight: 600; color: var(--color-text); margin-bottom: 8px;">Tu verifici și aprobi</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.5;">
					Niciun email trimis, nicio decizie luată fără confirmarea ta explicită.
				</div>
			</div>
		</div>
	</div>
</section>

<!-- DEMO TEASER -->
<section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Demo
	</p>
	<div
		style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 8px; padding: 28px 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;"
	>
		<div style="max-width: 440px;">
			<h2 style="font-size: 20px; font-weight: 600; color: var(--color-text); margin: 0 0 10px;">
				Atelier Nova SRL — 18 documente procesate
			</h2>
			<p style="color: var(--color-text-muted); font-size: 14px; line-height: 1.6; margin: 0 0 20px;">
				O firmă de design interior din Pitești primește facturi de la furnizori, cereri de la contabil,
				oferte, contracte și emailuri de la clienți. NovAI Desk procesează totul într-un singur spațiu de lucru.
			</p>
			<a
				href="/demo"
				style="display: inline-block; background: var(--color-action); color: var(--color-text); text-decoration: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; border: 1px solid var(--color-stroke-light);"
			>
				Explorează demo-ul
			</a>
		</div>
		<div
			style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 16px 20px; min-width: 240px;"
		>
			<div style="font-size: 12px; color: var(--color-text-muted); margin-bottom: 12px; letter-spacing: 0.05em; text-transform: uppercase;">Compania demo</div>
			<div style="font-weight: 600; color: var(--color-text); margin-bottom: 4px;">Atelier Nova SRL</div>
			<div style="font-size: 13px; color: var(--color-text-muted);">Design interior · Pitești · 12 angajați</div>
			<hr style="border: none; border-top: 1px solid var(--color-stroke); margin: 12px 0;" />
			<div style="font-size: 13px; color: var(--color-text-muted); line-height: 1.7;">
				18 documente procesate<br />
				Toate datele sunt sintetice
			</div>
		</div>
	</div>
</section>

<!-- TRUST -->
<section
	style="background: var(--color-data); border-top: 1px solid var(--color-stroke); border-bottom: 1px solid var(--color-stroke);"
>
	<div style="max-width: 1100px; margin: 0 auto; padding: 60px 24px;">
		<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
			Principii de bază
		</p>
		<h2 style="font-size: 24px; font-weight: 600; color: var(--color-text); margin: 0 0 32px;">
			AI pregătește. Omul decide.
		</h2>
		<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
			{#each [
				'Nicio trimitere automată de emailuri',
				'Aprobare umană obligatorie pentru orice acțiune',
				'Jurnal de audit pentru fiecare decizie',
				'Răspunsuri bazate exclusiv pe documentele tale',
				'Nicio integrare cu ANAF în versiunea actuală',
				'Date sintetice în demo — datele reale rămân private'
			] as item}
				<div
					style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 14px 16px;"
				>
					<div style="font-size: 14px; color: var(--color-text); line-height: 1.5;">{item}</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- FOOTER -->
<footer style="max-width: 1100px; margin: 0 auto; padding: 40px 24px;">
	<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
		<div>
			<div style="font-weight: 600; color: var(--color-text); margin-bottom: 4px;">NovAI Desk</div>
			<div style="font-size: 13px; color: var(--color-text-muted);">Spațiu de lucru AI privat pentru firme românești.</div>
		</div>
		<div style="display: flex; gap: 20px; align-items: center;">
			<a href="/about" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Despre</a>
			<a href="/demo" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Demo</a>
			<a href="/app/inbox" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Aplicație</a>
		</div>
	</div>
</footer>
