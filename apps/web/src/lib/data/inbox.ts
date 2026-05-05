export type DocType =
	| 'Supplier Invoice'
	| 'Accountant Request'
	| 'Client Request'
	| 'Supplier Contract'
	| 'Supplier Offer'
	| 'HR Policy'
	| 'Internal Procedure'
	| 'Price List';

export type Urgency = 'High' | 'Medium' | 'Low';

export type ApprovalState = 'Pending Review' | 'Approved' | 'Archived';

export interface ExtractedField {
	label: string;
	value: string;
}

export interface AuditEvent {
	timestamp: string;
	event: string;
}

export interface InboxDoc {
	id: string;
	filename: string;
	type: DocType;
	urgency: Urgency;
	summary: string;
	suggestedAction: string;
	fields: ExtractedField[];
	missingFields: string[];
	riskFlags: string[];
	approval: ApprovalState;
	audit: AuditEvent[];
	rawContent: string;
}

export const INBOX_DOCS: InboxDoc[] = [
	{
		id: 'invoice_lumina_design_2026_0041',
		filename: 'invoice_lumina_design_2026_0041.pdf',
		type: 'Supplier Invoice',
		urgency: 'High',
		summary:
			'Supplier invoice from Lumina Design SRL for LED decorative panels and accessories, total 3,046.40 RON, due on 12.05.2026. The internal purchase order reference is missing.',
		suggestedAction:
			'Ask supplier or internal team to confirm the purchase order reference, then forward to accountant.',
		fields: [
			{ label: 'Supplier', value: 'Lumina Design SRL' },
			{ label: 'Supplier CUI', value: 'RO00000001' },
			{ label: 'Invoice number', value: 'LD 0041' },
			{ label: 'Invoice date', value: '28.04.2026' },
			{ label: 'Due date', value: '12.05.2026' },
			{ label: 'Total amount', value: '3,046.40 RON' },
			{ label: 'VAT', value: '486.40 RON' },
			{ label: 'Currency', value: 'RON' },
			{ label: 'IBAN', value: 'RO00BANK0000000000000001' }
		],
		missingFields: ['Internal purchase order reference'],
		riskFlags: [],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 09:14', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 09:14', event: 'Fields extracted — 1 missing field flagged' },
			{ timestamp: '2026-05-05 09:14', event: 'Awaiting human review' }
		],
		rawContent: `Factura seria LD nr. 0041
Data emiterii: 28.04.2026
Furnizor: Lumina Design SRL
CUI: RO00000001
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse:
1. Panouri LED decorative model Aurora, 12 buc, 185 RON/buc
2. Cablu alimentare și accesorii montaj, 1 set, 340 RON

Subtotal: 2.560 RON
TVA: 486,40 RON
Total de plată: 3.046,40 RON
Scadență: 12.05.2026
IBAN: RO00BANK0000000000000001

Mențiune: Comanda internă nu este trecută pe factură.`
	},
	{
		id: 'email_accountant_missing_docs_april',
		filename: 'email_accountant_missing_docs_april.txt',
		type: 'Accountant Request',
		urgency: 'High',
		summary:
			'The accountant requests four missing April documents by 10 May, including supplier invoices, payment confirmation, a signed client contract, and approval explanation for SoftCloud.',
		suggestedAction: 'Collect the four requested documents and reply to the accountant before 10 May.',
		fields: [
			{ label: 'Requester', value: 'Mihai (external accountant)' },
			{ label: 'Deadline', value: '10 mai 2026' },
			{
				label: 'Documents requested',
				value:
					'Factura Lumina Design SRL · Confirmare plată PrintStudio · Contract Showroom Pitești · Explicație SoftCloud'
			}
		],
		missingFields: [],
		riskFlags: ['Deadline: 10 May — 5 days remaining'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 08:52', event: 'Email received and classified by AI' },
			{ timestamp: '2026-05-05 08:52', event: 'Four requested documents identified' },
			{ timestamp: '2026-05-05 08:52', event: 'Deadline flag set: 10 May' },
			{ timestamp: '2026-05-05 08:52', event: 'Awaiting human review' }
		],
		rawContent: `Subiect: Documente lipsă pentru luna aprilie

Bună, Irina,

Pentru închiderea lunii aprilie am nevoie de următoarele documente:

1. Factura de la Lumina Design SRL pentru panourile LED.
2. Confirmarea plății către PrintStudio pentru materialele promoționale.
3. Contractul semnat cu clientul pentru proiectul Showroom Pitești.
4. Explicație pentru factura SoftCloud, deoarece nu apare persoana care a aprobat abonamentul.

Te rog să mi le trimiți până pe 10 mai ca să putem finaliza raportarea la timp.

Mulțumesc,
Mihai`
	},
	{
		id: 'email_client_apartament_bucuresti',
		filename: 'email_client_apartament_bucuresti.txt',
		type: 'Client Request',
		urgency: 'Medium',
		summary:
			'Potential client asks for an interior design offer for a 78 sqm apartment in Bucharest, with a desired start in June. They need a reply explaining required information and estimated cost.',
		suggestedAction:
			'Send a polite reply asking for floor plan, photos, preferred style, budget range, and desired level of service. Include a rough starting price based on the service price list if available.',
		fields: [
			{ label: 'Requester', value: 'Radu Enache' },
			{ label: 'Request type', value: 'Interior design offer' },
			{ label: 'Location', value: 'București' },
			{ label: 'Size', value: 'approx. 78 sqm, 3 rooms' },
			{ label: 'Desired start', value: 'Iunie 2026' },
			{
				label: 'Services requested',
				value: 'consultanță design interior · propunere cromatică · recomandări mobilier · coordonare furnizori'
			}
		],
		missingFields: ['Floor plan', 'Photos', 'Style preference', 'Budget range'],
		riskFlags: [],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 10:03', event: 'Email received and classified by AI' },
			{ timestamp: '2026-05-05 10:03', event: 'Client request details extracted' },
			{ timestamp: '2026-05-05 10:03', event: 'Missing info flagged: 4 items needed for offer' },
			{ timestamp: '2026-05-05 10:03', event: 'Awaiting human review' }
		],
		rawContent: `Subiect: Cerere ofertă amenajare apartament 3 camere

Bună ziua,

Am găsit portofoliul Atelier Nova și am dori o ofertă pentru amenajarea unui apartament de 3 camere în București, aproximativ 78 mp.

Ne interesează:
- consultanță design interior
- propunere cromatică
- recomandări mobilier
- eventual coordonare furnizori

Am vrea să începem în luna iunie. Ne puteți spune ce informații aveți nevoie și care este un cost estimativ?

Mulțumesc,
Radu Enache`
	},
	{
		id: 'contract_supplier_lumina_design',
		filename: 'contract_supplier_lumina_design.txt',
		type: 'Supplier Contract',
		urgency: 'Low',
		summary:
			'Supplier contract with Lumina Design SRL for lighting products. Invoices must be paid within 14 calendar days, delivery should happen within 7 working days after order confirmation, and late payment penalties may apply after more than 10 days.',
		suggestedAction:
			'Note the 14-day payment term and ensure the outstanding invoice (LD 0041) is settled before the due date to avoid penalties.',
		fields: [
			{ label: 'Supplier', value: 'Lumina Design SRL' },
			{ label: 'Client', value: 'Atelier Nova SRL' },
			{ label: 'Contract number', value: '12 din 15.03.2026' },
			{ label: 'Valid until', value: '31.12.2026' },
			{ label: 'Payment terms', value: '14 zile calendaristice de la emiterea facturii' },
			{ label: 'Delivery', value: '7 zile lucrătoare de la confirmarea comenzii' },
			{ label: 'Late payment penalty', value: '0.05% pe zi din suma restantă (după 10 zile)' },
			{ label: 'Termination notice', value: '30 de zile scris' }
		],
		missingFields: [],
		riskFlags: [
			'Late payment penalties after 10 days',
			'Renewal requires written agreement',
			'Termination requires 30 days notice'
		],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 07:30', event: 'Contract received and classified by AI' },
			{ timestamp: '2026-05-05 07:30', event: 'Key terms extracted' },
			{
				timestamp: '2026-05-05 07:30',
				event: '3 risk flags identified: penalties, renewal, termination'
			},
			{ timestamp: '2026-05-05 07:30', event: 'Awaiting human review' }
		],
		rawContent: `Contract de colaborare nr. 12 din 15.03.2026

Părți:
Lumina Design SRL, în calitate de furnizor
Atelier Nova SRL, în calitate de beneficiar

Obiect:
Furnizarea de corpuri de iluminat decorative, panouri LED și accesorii pentru proiectele Atelier Nova.

Termen de livrare:
Furnizorul livrează produsele în termen de 7 zile lucrătoare de la confirmarea comenzii.

Plată:
Beneficiarul achită facturile în termen de 14 zile calendaristice de la data emiterii facturii.

Penalități:
Pentru întârzieri la plată mai mari de 10 zile, se pot aplica penalități de 0,05% pe zi din suma restantă.

Durată:
Contractul este valabil până la 31.12.2026 și se poate prelungi prin acord scris.

Încetare:
Oricare parte poate denunța contractul cu notificare scrisă transmisă cu 30 de zile înainte.`
	},

	// === Supplier Invoices ===

	{
		id: 'invoice_mobila_artisan_2026_0187',
		filename: 'invoice_mobila_artisan_2026_0187.pdf',
		type: 'Supplier Invoice',
		urgency: 'Medium',
		summary:
			'Invoice from Mobila Artisan SRL for custom shelving modules and assembly, total 3,160 RON, due 21.05.2026. Delivery was confirmed verbally but no signed acceptance protocol is attached.',
		suggestedAction:
			'Request a signed acceptance protocol from Mobila Artisan SRL before approving payment.',
		fields: [
			{ label: 'Supplier', value: 'Mobila Artisan SRL' },
			{ label: 'Supplier CUI', value: 'RO00000003' },
			{ label: 'IBAN', value: 'RO00BANK0000000000000003' },
			{ label: 'Invoice number', value: 'MA 0187' },
			{ label: 'Invoice date', value: '30.04.2026' },
			{ label: 'Due date', value: '21.05.2026' },
			{ label: 'Total amount', value: '3,160.00 RON' },
			{ label: 'VAT', value: '504.00 RON (19%)' },
			{ label: 'Currency', value: 'RON' }
		],
		missingFields: ['Signed acceptance protocol for delivery'],
		riskFlags: [],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 11:20', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 11:20', event: 'Fields extracted — 1 missing field flagged' },
			{ timestamp: '2026-05-05 11:20', event: 'Awaiting human review' }
		],
		rawContent: `Factura seria MA nr. 0187
Data emiterii: 30.04.2026
Furnizor: Mobila Artisan SRL
CUI: RO00000003
IBAN: RO00BANK0000000000000003
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse și servicii:
1. Rafturi personalizate model Industrial Slim, 4 module, 720 RON/buc = 2.880 RON
2. Montaj și fixare la locație, 1 serviciu = 280 RON

Subtotal: 3.160 RON (TVA inclus 504 RON)
Total de plată: 3.160,00 RON
Scadență: 21.05.2026

Notă: Livrarea a fost confirmată telefonic pe 29.04.2026. Procesul-verbal de recepție nu a fost semnat.`
	},

	{
		id: 'invoice_printstudio_2026_0098',
		filename: 'invoice_printstudio_2026_0098.pdf',
		type: 'Supplier Invoice',
		urgency: 'Medium',
		summary:
			'Invoice from PrintStudio Media SRL for promotional materials (catalogs, business cards), total 848 RON. Payment was made on 02.05.2026 but proof of payment has not been forwarded to the accountant.',
		suggestedAction:
			'Locate the bank payment confirmation from 02.05.2026 and send it to accountant Mihai.',
		fields: [
			{ label: 'Supplier', value: 'PrintStudio Media SRL' },
			{ label: 'Supplier CUI', value: 'RO00000004' },
			{ label: 'Invoice number', value: 'PS 0098' },
			{ label: 'Invoice date', value: '25.04.2026' },
			{ label: 'Payment status', value: 'Plătită 02.05.2026 (confirmat intern)' },
			{ label: 'Total amount', value: '848.00 RON' },
			{ label: 'Currency', value: 'RON' }
		],
		missingFields: ['Payment confirmation forwarded to accountant'],
		riskFlags: ['Accountant awaiting proof of payment — needed for April close'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 08:55', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 08:55', event: 'Fields extracted — payment confirmation gap flagged' },
			{
				timestamp: '2026-05-05 08:55',
				event: 'Linked to accountant request: email_accountant_missing_docs_april'
			},
			{ timestamp: '2026-05-05 08:55', event: 'Awaiting human review' }
		],
		rawContent: `Factura seria PS nr. 0098
Data emiterii: 25.04.2026
Furnizor: PrintStudio Media SRL
CUI: RO00000004
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse:
1. Cataloage produs format A4, 200 exemplare, 2,20 RON/buc = 440 RON
2. Cărți de vizită premium, 500 buc, 0,60 RON/buc = 300 RON
3. Design grafic și pregătire tipărire, 1 serviciu = 108 RON

Total: 848,00 RON (TVA inclus)
Mențiune: Factura a fost achitată prin ordin bancar pe 02.05.2026.
Confirmarea plății nu a fost transmisă contabilului.`
	},

	{
		id: 'invoice_curier_rapid_2026_1142',
		filename: 'invoice_curier_rapid_2026_1142.pdf',
		type: 'Supplier Invoice',
		urgency: 'Low',
		summary:
			'Invoice from Curier Rapid Express SRL for delivery services in April 2026, total 441 RON, due 15.05.2026. One delivery (position 3) is disputed — the recipient claims the package was incomplete.',
		suggestedAction:
			'Clarify the disputed delivery (position 3) with the courier before approving the invoice.',
		fields: [
			{ label: 'Supplier', value: 'Curier Rapid Express SRL' },
			{ label: 'Supplier CUI', value: 'RO00000005' },
			{ label: 'Invoice number', value: 'CR 1142' },
			{ label: 'Invoice date', value: '30.04.2026' },
			{ label: 'Due date', value: '15.05.2026' },
			{ label: 'Total amount', value: '441.00 RON' },
			{ label: 'Currency', value: 'RON' }
		],
		missingFields: [],
		riskFlags: ['Position 3 disputed — recipient claims incomplete package'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 09:40', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 09:40', event: 'Fields extracted — dispute flag on position 3' },
			{ timestamp: '2026-05-05 09:40', event: 'Awaiting human review' }
		],
		rawContent: `Factura seria CR nr. 1142
Data emiterii: 30.04.2026
Furnizor: Curier Rapid Express SRL
CUI: RO00000005
Client: Atelier Nova SRL
CUI Client: RO00000002

Servicii livrare aprilie 2026:
1. Livrare pachet mobilier mic (01.04.2026) — 85 RON
2. Livrare mostre materiale textile (10.04.2026) — 95 RON
3. Livrare comandă client Ionescu (18.04.2026) — 145 RON [DISPUTAT]
4. Livrare accesorii LED (24.04.2026) — 116 RON

Total: 441,00 RON (TVA inclus)
Scadență: 15.05.2026

Notă internă: Clientul Ionescu a reclamat că pachetul din 18.04 era incomplet. Situația nu este clarificată.`
	},

	{
		id: 'invoice_softcloud_2026_0520',
		filename: 'invoice_softcloud_2026_0520.pdf',
		type: 'Supplier Invoice',
		urgency: 'High',
		summary:
			'Monthly subscription invoice from SoftCloud Solutions SRL for cloud hosting and backup, 220 RON, due 18.05.2026. The accountant flagged this — no internal record of who approved the subscription.',
		suggestedAction:
			'Identify who approved the SoftCloud subscription and provide a written explanation to the accountant before 10 May.',
		fields: [
			{ label: 'Supplier', value: 'SoftCloud Solutions SRL' },
			{ label: 'Supplier CUI', value: 'RO00000006' },
			{ label: 'Invoice number', value: 'SC 0520' },
			{ label: 'Invoice date', value: '01.05.2026' },
			{ label: 'Due date', value: '18.05.2026' },
			{ label: 'Total amount', value: '220.00 RON' },
			{ label: 'Service', value: 'Abonament lunar cloud hosting + backup' },
			{ label: 'Currency', value: 'RON' }
		],
		missingFields: ['Name of person who approved the subscription'],
		riskFlags: [
			'Accountant flagged: no approval record on file',
			'Linked to accountant deadline: 10 May'
		],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 09:00', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 09:00', event: 'Fields extracted — missing approval flag identified' },
			{
				timestamp: '2026-05-05 09:00',
				event: 'Linked to accountant request: email_accountant_missing_docs_april (pct. 4)'
			},
			{ timestamp: '2026-05-05 09:00', event: 'Awaiting human review' }
		],
		rawContent: `Factura seria SC nr. 0520
Data emiterii: 01.05.2026
Furnizor: SoftCloud Solutions SRL
CUI: RO00000006
Client: Atelier Nova SRL
CUI Client: RO00000002

Servicii:
1. Abonament cloud hosting Standard — mai 2026: 150 RON
2. Serviciu backup automat zilnic — mai 2026: 70 RON

Total: 220,00 RON (TVA inclus)
Scadență: 18.05.2026

Mențiune: Nu există în evidențele interne o aprobare scrisă sau un e-mail de confirmare pentru acest abonament. Contabilul a solicitat clarificări.`
	},

	// === Client Emails ===

	{
		id: 'email_client_showroom_pitesti',
		filename: 'email_client_showroom_pitesti.txt',
		type: 'Client Request',
		urgency: 'Medium',
		summary:
			'Existing client asks for a status update on Showroom Pitești renovation phase 1. The client mentions 15 May as the expected deadline, but the contract specifies 30 May for phase 1.',
		suggestedAction:
			'Review the contract milestone dates and reply with the correct schedule, clarifying the 30 May phase 1 deadline.',
		fields: [
			{ label: 'Sender', value: 'Andrei Popescu — Constructiv Design SRL' },
			{ label: 'Topic', value: 'Status update Showroom Pitești — Faza 1' },
			{ label: 'Date client expects', value: '15.05.2026' },
			{ label: 'Contract phase 1 deadline', value: '30.05.2026' }
		],
		missingFields: [],
		riskFlags: ['Client expects phase 1 by 15 May — contract says 30 May — clarification needed'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 10:30', event: 'Email received and classified by AI' },
			{ timestamp: '2026-05-05 10:30', event: 'Client request details extracted' },
			{
				timestamp: '2026-05-05 10:30',
				event: 'Date mismatch flagged: client expectation vs contract milestone'
			},
			{ timestamp: '2026-05-05 10:30', event: 'Awaiting human review' }
		],
		rawContent: `Subiect: Update proiect Showroom Pitești — stadiu lucrări

Bună ziua,

Vă contactăm în legătură cu proiectul de amenajare a showroom-ului nostru din Pitești.

Am dori să știm stadiul actual al lucrărilor și dacă Faza 1 (finisaje pereți și pardoseală) va fi gata până pe 15 mai, conform înțelegerii noastre.

Avem o prezentare de produse planificată la mijlocul lui mai și ar fi important să știm dacă putem conta pe spațiu.

Vă mulțumim pentru un răspuns rapid.

Cu stimă,
Andrei Popescu
Constructiv Design SRL`
	},

	{
		id: 'email_client_intarziere_livrare',
		filename: 'email_client_intarziere_livrare.txt',
		type: 'Client Request',
		urgency: 'High',
		summary:
			'Client complaint about a 5-day delay on a custom furniture delivery. The client is polite but firm, and requests compensation or a partial discount on a future order.',
		suggestedAction:
			'Draft a reply acknowledging the delay, explaining the cause, and proposing a goodwill gesture such as a discount on the next order.',
		fields: [
			{ label: 'Sender', value: 'Maria Dumitrescu' },
			{ label: 'Topic', value: 'Complaint: delivery delay — 5 days' },
			{ label: 'Order', value: 'Mobilier personalizat — comandă 10.04.2026' },
			{ label: 'Expected delivery', value: '29.04.2026' },
			{ label: 'Actual delivery', value: '04.05.2026' },
			{ label: 'Request', value: 'Compensation or partial discount' }
		],
		missingFields: [],
		riskFlags: ['Client requesting compensation — respond promptly to avoid escalation'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 11:05', event: 'Email received and classified by AI' },
			{ timestamp: '2026-05-05 11:05', event: 'Complaint and compensation request identified' },
			{ timestamp: '2026-05-05 11:05', event: 'High urgency — risk of client dissatisfaction' },
			{ timestamp: '2026-05-05 11:05', event: 'Awaiting human review' }
		],
		rawContent: `Subiect: Întârziere livrare comandă mobilier

Bună ziua,

Comanda noastră de mobilier personalizat (plasată pe 10 aprilie) trebuia livrată pe 29 aprilie, conform confirmării primite. Livrarea a avut loc abia pe 4 mai, cu o întârziere de 5 zile.

Înțelegem că pot apărea situații neprevăzute, dar ne-a afectat planificarea lucrărilor la sediu.

Am dori să știm care a fost cauza întârzierii și dacă există posibilitatea unui gest de bună-voință din partea Atelier Nova — fie o reducere parțială pe această comandă, fie un discount pentru o viitoare colaborare.

Așteptăm răspunsul dumneavoastră.

Cu respect,
Maria Dumitrescu`
	},

	// === Supplier Offers ===

	{
		id: 'offer_lumina_led_panels',
		filename: 'offer_lumina_led_panels.txt',
		type: 'Supplier Offer',
		urgency: 'Low',
		summary:
			'Lumina Design SRL offers new generation LED Aurora Pro panels at a 12% discount, valid until 31.05.2026. The discount applies only on minimum orders of 30 units.',
		suggestedAction:
			'Check if current or upcoming projects require 30+ LED panels. If yes, confirm order before 31 May to lock in the 12% discount.',
		fields: [
			{ label: 'Supplier', value: 'Lumina Design SRL' },
			{ label: 'Product', value: 'Panouri LED Aurora Pro — generație nouă' },
			{ label: 'Discount', value: '12%' },
			{ label: 'Minimum order', value: '30 bucăți' },
			{ label: 'Offer valid until', value: '31.05.2026' },
			{ label: 'List price', value: '195 RON/buc' },
			{ label: 'Discounted price', value: '171.60 RON/buc' }
		],
		missingFields: [],
		riskFlags: ['Discount requires minimum 30-unit order — verify demand before committing'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 09:55', event: 'Offer received and classified by AI' },
			{ timestamp: '2026-05-05 09:55', event: 'Discount condition and deadline extracted' },
			{ timestamp: '2026-05-05 09:55', event: 'Minimum order requirement flagged' },
			{ timestamp: '2026-05-05 09:55', event: 'Awaiting human review' }
		],
		rawContent: `Ofertă comercială
Data: 02.05.2026
De la: Lumina Design SRL
Către: Atelier Nova SRL

Stimate partener,

Vă informăm că am lansat o nouă generație de panouri LED Aurora Pro, cu eficiență energetică îmbunătățită și profil mai subțire față de modelul anterior.

Ofertă specială de lansare:
- Preț de listă: 195 RON/buc
- Discount partener: 12%
- Preț net: 171,60 RON/buc
- Valabilitate ofertă: până la 31.05.2026

Condiție: reducerea se aplică la comenzi de minimum 30 bucăți.
Pentru cantități sub 30 de bucăți, prețul de listă standard rămâne aplicabil.

Suntem la dispoziție pentru detalii tehnice sau un demo la sediul dumneavoastră.

Cu stimă,
Echipa comercială Lumina Design SRL`
	},

	{
		id: 'offer_mobila_custom_shelves',
		filename: 'offer_mobila_custom_shelves.txt',
		type: 'Supplier Offer',
		urgency: 'Low',
		summary:
			"Mobila Artisan SRL proposes custom shelving for a hypothetical second showroom, with a 6-week lead time. This lead time is likely longer than Atelier Nova's typical project timeline.",
		suggestedAction:
			'Evaluate whether the 6-week lead time is compatible with any planned projects. No action required if no second showroom is planned.',
		fields: [
			{ label: 'Supplier', value: 'Mobila Artisan SRL' },
			{ label: 'Product', value: 'Rafturi personalizate pentru showroom secundar' },
			{ label: 'Lead time', value: '6 săptămâni de la confirmare' },
			{ label: 'Unit price (sample)', value: '680 RON/modul' },
			{ label: 'Minimum order (sample)', value: '8 module' },
			{ label: 'Estimated total (sample)', value: '5,440 RON' }
		],
		missingFields: [],
		riskFlags: ['Lead time 6 weeks — may not fit standard project timelines'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 10:15', event: 'Offer received and classified by AI' },
			{ timestamp: '2026-05-05 10:15', event: 'Lead time and pricing extracted' },
			{ timestamp: '2026-05-05 10:15', event: 'Lead time flag: 6 weeks vs typical project window' },
			{ timestamp: '2026-05-05 10:15', event: 'Awaiting human review' }
		],
		rawContent: `Ofertă mobilier personalizat — Showroom secundar
Data: 04.05.2026
De la: Mobila Artisan SRL
Către: Atelier Nova SRL

Bună ziua,

Urmând discuția noastră anterioară despre extinderea spațiilor de prezentare, vă transmitem o ofertă orientativă pentru amenajarea unui showroom secundar cu sistem de rafturi personalizate.

Configurație propusă (orientativă):
- Modul raft personalizat 200×40×180 cm (finisaj stejar natural): 680 RON/buc
- Cantitate minimă estimată: 8 module
- Total orientativ: 5.440 RON + TVA

Termen de execuție: 6 săptămâni de la confirmarea comenzii și semnarea contractului.
Prețurile sunt valabile 30 de zile de la data ofertei.

Suntem disponibili pentru o întâlnire de detaliere.

Cu respect,
Mobila Artisan SRL`
	},

	// === Client Contract ===

	{
		id: 'contract_client_showroom_renovation',
		filename: 'contract_client_showroom_renovation.txt',
		type: 'Supplier Contract',
		urgency: 'Medium',
		summary:
			'Client contract for full renovation of a 220 sqm showroom in Pitești across 3 milestone phases, 15.04.2026–30.06.2026. Penalty clause (0.1%/day) is twice as strict as the supplier-side Lumina Design contract (0.05%/day).',
		suggestedAction:
			'Monitor phase 1 progress toward the 30 May milestone. Note that Atelier Nova is exposed asymmetrically — client penalties are double the supplier penalties.',
		fields: [
			{ label: 'Client', value: 'Constructiv Design SRL' },
			{ label: 'Client CUI', value: 'RO00000007' },
			{ label: 'Contract number', value: '07 din 10.04.2026' },
			{ label: 'Scope', value: 'Amenajare showroom 220 mp, Pitești — 3 faze' },
			{ label: 'Project start', value: '15.04.2026' },
			{ label: 'Project end', value: '30.06.2026' },
			{ label: 'Phase 1 deadline', value: '30.05.2026' },
			{ label: 'Payment — advance', value: '40% la semnare' },
			{ label: 'Payment — mid-project', value: '40% la finalizarea Fazei 2' },
			{ label: 'Payment — final', value: '20% la recepție finală' },
			{ label: 'Late penalty', value: '0.1%/zi pentru depășirea termenului 30.06.2026' }
		],
		missingFields: [],
		riskFlags: [
			'Client penalty 0.1%/day — stricter than supplier-side Lumina contract (0.05%/day)',
			'Phase 1 deadline: 30.05.2026 — monitor progress',
			'Client email references 15 May — does not match contract milestone'
		],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 07:45', event: 'Contract received and classified by AI' },
			{ timestamp: '2026-05-05 07:45', event: 'Key terms extracted — 3 risk flags identified' },
			{ timestamp: '2026-05-05 07:45', event: 'Penalty asymmetry flagged vs Lumina Design contract' },
			{ timestamp: '2026-05-05 07:45', event: 'Awaiting human review' }
		],
		rawContent: `Contract de prestări servicii nr. 07 din 10.04.2026

Părți:
Atelier Nova SRL (prestator), CUI RO00000002
Constructiv Design SRL (beneficiar), CUI RO00000007

Obiect:
Amenajare completă showroom Pitești, suprafață 220 mp, conform proiectului agreat.

Faze și termene:
- Faza 1 (finisaje pereți și pardoseală): finalizare până la 30.05.2026
- Faza 2 (mobilier și iluminat): finalizare până la 20.06.2026
- Faza 3 (finisaje finale și recepție): finalizare până la 30.06.2026

Prețul total: 68.000 RON + TVA

Plată:
- 40% avans la semnarea contractului
- 40% la finalizarea Fazei 2
- 20% la recepția finală

Penalități:
În cazul depășirii termenului final (30.06.2026), se aplică penalități de 0,1% pe zi din valoarea contractului rămas de executat.

Încetare:
Oricare parte poate rezilia contractul cu notificare scrisă de 15 zile.`
	},

	// === Internal Documents ===

	{
		id: 'policy_hr_remote_work',
		filename: 'policy_hr_remote_work.txt',
		type: 'HR Policy',
		urgency: 'Low',
		summary:
			'Internal HR policy draft for remote work, limiting remote days to a maximum of 2 per week per employee. The document has not yet been officially approved or distributed.',
		suggestedAction:
			'Review and sign off on this draft. Decide whether to distribute to all employees or file internally only.',
		fields: [
			{ label: 'Document type', value: 'Politică internă HR — draft' },
			{ label: 'Version', value: 'Draft v1 — mai 2026' },
			{ label: 'Max remote days', value: '2 zile/săptămână per angajat' },
			{ label: 'Eligibility', value: 'Minimum 6 luni vechime' },
			{ label: 'Approval required from', value: 'Manager direct' }
		],
		missingFields: ['Official approval signature', 'Distribution list'],
		riskFlags: [],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 08:00', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 08:00', event: 'HR policy fields extracted' },
			{ timestamp: '2026-05-05 08:00', event: 'Missing: approval signature and distribution list' },
			{ timestamp: '2026-05-05 08:00', event: 'Awaiting human review' }
		],
		rawContent: `Politică lucru de la distanță (telemuncă)
Versiune: Draft v1 — mai 2026
Atelier Nova SRL

1. Scop
Această politică reglementează condițiile în care angajații Atelier Nova SRL pot desfășura activitate în regim de telemuncă.

2. Eligibilitate
Pot beneficia de telemuncă angajații cu minimum 6 luni vechime în cadrul companiei, cu acordul managerului direct și în măsura în care natura activității permite lucrul de la distanță.

3. Număr maxim de zile
Fiecare angajat eligibil poate lucra de la distanță maximum 2 zile pe săptămână.

4. Procedura de aprobare
Solicitarea se face în scris (email sau formular intern) cu cel puțin 3 zile lucrătoare înainte. Managerul direct aprobă sau refuză în termen de 1 zi lucrătoare.

5. Cerințe tehnice
Angajatul trebuie să dispună de conexiune stabilă la internet și acces securizat la sistemele companiei.

Notă: Acest document nu a fost distribuit oficial. Urmează aprobare și publicare internă.`
	},

	{
		id: 'procedure_client_project_intake',
		filename: 'procedure_client_project_intake.txt',
		type: 'Internal Procedure',
		urgency: 'Low',
		summary:
			'Step-by-step procedure for onboarding a new client project, from consultation to kickoff. Step 4 references a "standard contract template" that does not yet exist as a document in the archive.',
		suggestedAction:
			'Create or locate the standard contract template referenced in step 4 and link it to this procedure.',
		fields: [
			{ label: 'Document type', value: 'Procedură internă' },
			{ label: 'Version', value: 'v1 — mai 2026' },
			{
				label: 'Steps',
				value: '5: consultație → vizită → ofertă → contract → kickoff'
			}
		],
		missingFields: ['Standard contract template (referenced in step 4 — not found in archive)'],
		riskFlags: [],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 08:10', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 08:10', event: 'Procedure steps extracted' },
			{
				timestamp: '2026-05-05 08:10',
				event: 'Missing reference: standard contract template (step 4)'
			},
			{ timestamp: '2026-05-05 08:10', event: 'Awaiting human review' }
		],
		rawContent: `Procedură preluare proiect client nou
Versiune: v1 — mai 2026
Atelier Nova SRL

Scop: Standardizarea procesului de preluare și demarare a unui proiect client nou.

Pasul 1 — Consultație inițială
Întâlnire (fizică sau online) pentru înțelegerea nevoilor clientului. Durata: 1–2 ore. Responsabil: designer principal.

Pasul 2 — Vizită la locație
Evaluare spațiu, măsurători, documentare foto. Responsabil: echipă tehnică. Durată estimată: 0,5–1 zi.

Pasul 3 — Elaborare ofertă
Pe baza informațiilor din pasul 2, se elaborează oferta detaliată cu prețuri și termene. Responsabil: manager proiect. Termen: max 5 zile lucrătoare.

Pasul 4 — Semnare contract
Se utilizează șablonul standard de contract (a se vedea: contract_standard_atelier_nova.docx). Se transmite clientului pentru revizuire cu 2 zile înainte de întâlnire.

ATENȚIE: Documentul șablon contract standard nu a fost identificat în arhiva curentă.

Pasul 5 — Kickoff proiect
Întâlnire de lansare cu echipa internă și clientul. Se stabilesc responsabilitățile, calendarul și canalele de comunicare.`
	},

	{
		id: 'price_list_services_2026',
		filename: 'price_list_services_2026.txt',
		type: 'Price List',
		urgency: 'Low',
		summary:
			'Internal service price list for 2026 covering consultation, design, project management, and custom items. A footnote states prices are subject to revision after Q2 2026.',
		suggestedAction:
			'Approve this price list for internal use and schedule a Q2 revision meeting before 30 June.',
		fields: [
			{ label: 'Document type', value: 'Listă de prețuri servicii' },
			{ label: 'Valid from', value: '01.01.2026' },
			{ label: 'Currency', value: 'RON (fără TVA)' },
			{ label: 'Revision note', value: 'Prețurile pot fi revizuite după Q2 2026' }
		],
		missingFields: [],
		riskFlags: ['Prices subject to revision after Q2 2026 — schedule update before 30 June'],
		approval: 'Pending Review',
		audit: [
			{ timestamp: '2026-05-05 08:20', event: 'Document received and classified by AI' },
			{ timestamp: '2026-05-05 08:20', event: 'Pricing structure extracted' },
			{ timestamp: '2026-05-05 08:20', event: 'Q2 revision flag noted' },
			{ timestamp: '2026-05-05 08:20', event: 'Awaiting human review' }
		],
		rawContent: `Listă prețuri servicii 2026
Atelier Nova SRL
Valabilă de la 01.01.2026

Servicii de consultanță:
- Consultație inițială (1–2 ore): 300 RON
- Consultație extinsă cu documentare locație: 550 RON

Servicii de design:
- Concept design interior (1 spațiu): 1.200 RON
- Proiect complet design interior (1 spațiu, toate fazele): 3.500 RON
- Randare 3D (per cameră): 450 RON

Management de proiect:
- Coordonare proiect simplă (până la 100 mp): 2.500 RON
- Coordonare proiect complex (100–300 mp): 5.500 RON
- Supervizare lucrări (per zi de lucru): 350 RON

Articole personalizate:
- Mobilier la comandă: conform ofertă individuală
- Iluminat decorativ la comandă: conform ofertă individuală

Notă: Prețurile sunt exprimate fără TVA. TVA se adaugă conform legislației în vigoare (19%).

*Prețurile din această listă pot fi revizuite după Q2 2026 în funcție de evoluția costurilor de materiale și manoperă.*`
	}
];
