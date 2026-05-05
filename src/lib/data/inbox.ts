export type DocType =
	| 'Supplier Invoice'
	| 'Accountant Request'
	| 'Client Request'
	| 'Supplier Contract';

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
	}
];
