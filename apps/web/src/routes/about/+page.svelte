<svelte:head>
	<title>Despre NovAI Desk</title>
	<meta
		name="description"
		content="Cine a construit NovAI Desk, pentru cine este, ce face și ce nu face."
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
			<a href="/about" style="color: var(--color-text); text-decoration: none; font-size: 14px; font-weight: 500;">Despre</a>
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

<!-- HEADER -->
<section style="max-width: 800px; margin: 0 auto; padding: 64px 24px 48px;">
	<p style="color: var(--color-text-muted); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
		Despre proiect
	</p>
	<h1 style="font-size: clamp(24px, 4vw, 36px); font-weight: 700; color: var(--color-text); margin: 0 0 16px; line-height: 1.25;">
		NovAI Desk
	</h1>
	<p style="color: var(--color-text-muted); font-size: 16px; line-height: 1.7; max-width: 600px;">
		Un spațiu de lucru AI privat pentru firme mici și mijlocii din România. AI-ul pregătește.
		Omul decide.
	</p>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- CINE SUNTEM -->
<section style="max-width: 800px; margin: 0 auto; padding: 48px 24px;">
	<h2 style="font-size: 18px; font-weight: 600; color: var(--color-text); margin: 0 0 16px;">
		Cine a construit acest proiect
	</h2>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0 0 14px;">
		NovAI Desk este un proiect independent, construit ca prototip funcțional pentru a demonstra
		cum poate arăta un spațiu de lucru AI adaptat realității operaționale a firmelor românești.
	</p>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0;">
		Codul sursă și documentele de proiect vor fi disponibile pe
		<a
			href="https://github.com/csmcl"
			target="_blank"
			rel="noopener"
			style="color: var(--color-stroke-light); text-decoration: underline;"
		>GitHub</a>.
		Demo-ul folosește date sintetice — niciun document real al vreunei firme reale nu a fost
		utilizat în construcția sau testarea aplicației.
	</p>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- PENTRU CINE -->
<section style="max-width: 800px; margin: 0 auto; padding: 48px 24px;">
	<h2 style="font-size: 18px; font-weight: 600; color: var(--color-text); margin: 0 0 16px;">
		Pentru cine este
	</h2>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0 0 20px;">
		Firme mici și mijlocii din România cu 3–30 de angajați, care lucrează zilnic cu:
	</p>
	<ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
		{#each [
			'Facturi de la furnizori cu termene și câmpuri care trebuie verificate',
			'Cereri periodice de la contabil (balanță, TVA, declarații)',
			'Emailuri de la clienți care conțin cereri de ofertă sau actualizări de proiect',
			'Contracte cu furnizori sau clienți ce conțin clauze importante',
			'Oferte primite de la furnizori care necesită o decizie'
		] as item}
			<li
				style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 12px 16px; display: flex; gap: 10px; align-items: flex-start;"
			>
				<span style="color: var(--color-stroke-light); margin-top: 2px; flex-shrink: 0;">—</span>
				<span style="font-size: 14px; color: var(--color-text); line-height: 1.5;">{item}</span>
			</li>
		{/each}
	</ul>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- CE FACE -->
<section style="max-width: 800px; margin: 0 auto; padding: 48px 24px;">
	<h2 style="font-size: 18px; font-weight: 600; color: var(--color-text); margin: 0 0 16px;">
		Ce face
	</h2>
	<div style="display: flex; flex-direction: column; gap: 16px;">
		{#each [
			{
				label: 'AI Inbox',
				text: 'Fiecare document încărcat (PDF sau arhivă ZIP) este clasificat automat: tip, limbă, urgență. AI-ul extrage câmpurile relevante, rezumă conținutul și sugerează ce trebuie făcut.'
			},
			{
				label: 'Întreabă compania',
				text: 'Poți pune întrebări în limbaj natural despre documentele tale. Răspunsurile vin exclusiv din fișierele pe care le-ai încărcat — nu de pe internet.'
			},
			{
				label: 'Stare de recenzie',
				text: 'Fiecare document poate fi marcat: aprobat, necesită verificare sau respins. Starea este vizibilă în inbox și înregistrată în jurnalul de audit.'
			},
			{
				label: 'Descărcare arhivă demo',
				text: 'Poți descărca setul complet de documente PDF sintetice ale companiei Atelier Nova SRL și le poți încărca direct în aplicație pentru a testa fluxul complet.'
			}
		] as item}
			<div style="background: var(--color-main); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 16px 20px;">
				<div style="font-weight: 600; color: var(--color-text); font-size: 14px; margin-bottom: 6px;">{item.label}</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.6;">{item.text}</div>
			</div>
		{/each}
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- CE NU FACE -->
<section
	style="max-width: 800px; margin: 0 auto; padding: 48px 24px;"
>
	<h2 style="font-size: 18px; font-weight: 600; color: var(--color-text); margin: 0 0 8px;">
		Ce nu face
	</h2>
	<p style="color: var(--color-text-muted); font-size: 14px; line-height: 1.6; margin: 0 0 20px;">
		Limitele sunt deliberate, nu tehnice.
	</p>
	<div style="display: flex; flex-direction: column; gap: 10px;">
		{#each [
			{
				label: 'Nu trimite emailuri automat',
				text: 'Aplicația nu trimite niciun email fără confirmarea ta. Proiectele de răspuns sunt doar sugestii — tu apeși butonul de trimitere.'
			},
			{
				label: 'Nu se integrează cu ANAF',
				text: 'Nu există nicio conexiune cu sistemele ANAF, e-Factura sau orice altă platformă guvernamentală. Documentele rămân în spațiul tău local.'
			},
			{
				label: 'Nu fine-tunează modele pe datele tale',
				text: 'Documentele pe care le încarci nu sunt folosite pentru a antrena sau a ajusta modelele AI. Răspunsurile vin dintr-un model general, grouneded pe conținutul tău.'
			},
			{
				label: 'Nu ia decizii în locul tău',
				text: 'Orice sugestie — acțiune, răspuns, clasificare — necesită aprobarea ta. Jurnalul de audit înregistrează ce a sugerat AI-ul și ce ai decis tu.'
			}
		] as item}
			<div
				style="background: var(--color-data); border: 1px solid var(--color-stroke); border-radius: 6px; padding: 16px 20px; border-left: 3px solid var(--color-stroke-light);"
			>
				<div style="font-weight: 600; color: var(--color-text); font-size: 14px; margin-bottom: 6px;">{item.label}</div>
				<div style="font-size: 14px; color: var(--color-text-muted); line-height: 1.6;">{item.text}</div>
			</div>
		{/each}
	</div>
</section>

<hr style="border: none; border-top: 1px solid var(--color-stroke); opacity: 0.4; margin: 0 24px;" />

<!-- DATE SINTETICE -->
<section style="max-width: 800px; margin: 0 auto; padding: 48px 24px;">
	<h2 style="font-size: 18px; font-weight: 600; color: var(--color-text); margin: 0 0 16px;">
		Date sintetice și caractere de siguranță
	</h2>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0 0 14px;">
		Toate documentele din demo aparțin companiei fictive <strong style="color: var(--color-text);">Atelier Nova SRL</strong>
		și partenerilor ei sintetici. Nicio dată reală nu a fost folosită.
	</p>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0 0 14px;">
		Pentru a preveni ca datele sintetice să fie confundate cu date reale, câmpurile sensibile
		(CUI, IBAN, număr de telefon, număr de înregistrare la Registrul Comerțului) conțin caracterul
		<strong style="color: var(--color-text); font-family: monospace;">Ɛ</strong>
		(U+0190 LATIN CAPITAL LETTER OPEN E) — un caracter valid Unicode care nu apare în niciun
		identificator fiscal sau bancar real românesc.
	</p>
	<p style="color: var(--color-text-muted); font-size: 15px; line-height: 1.7; margin: 0;">
		Dacă vezi <code style="background: var(--color-data); padding: 1px 5px; border-radius: 3px; font-size: 13px;">Ɛ</code>
		într-un document din demo, știi că acel câmp este deliberat sintetic.
	</p>
</section>

<!-- FOOTER -->
<footer style="max-width: 800px; margin: 0 auto; padding: 40px 24px; border-top: 1px solid var(--color-stroke);">
	<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
		<div style="font-size: 13px; color: var(--color-text-muted);">NovAI Desk · proiect independent</div>
		<div style="display: flex; gap: 20px; align-items: center;">
			<a href="/" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Acasă</a>
			<a href="/demo" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Demo</a>
			<a href="/app/inbox" style="color: var(--color-text-muted); text-decoration: none; font-size: 13px;">Aplicație</a>
		</div>
	</div>
</footer>
