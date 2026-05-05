export interface QAResult {
	answer: string;
	sources: string[];
}

interface QAPair {
	keywords: string[];
	result: QAResult;
}

const QA_PAIRS: QAPair[] = [
	{
		keywords: ['urgent', 'urgente', 'urgenta', 'invoices', 'facturi', 'this week', 'saptamana'],
		result: {
			answer:
				'There are two high-urgency invoices this week. **invoice_softcloud_2026_0520.pdf** (220 RON, due 18 May) is flagged because no approval record exists for the subscription — the accountant is waiting for an explanation before 10 May. **invoice_lumina_design_2026_0041.pdf** (3,046.40 RON, due 12 May) is missing the internal purchase order reference. Both need attention before their due dates.',
			sources: ['invoice_softcloud_2026_0520.pdf', 'invoice_lumina_design_2026_0041.pdf']
		}
	},
	{
		keywords: ['accountant', 'contabil', 'contabilul', 'requested', 'cerut', 'solicitat'],
		result: {
			answer:
				'The accountant (Mihai) sent a request on 5 May with a **deadline of 10 May**. Four items are needed to close April: (1) the Lumina Design SRL invoice, (2) payment confirmation for PrintStudio, (3) the signed Showroom Pitești contract, and (4) a written explanation of who approved the SoftCloud subscription.',
			sources: ['email_accountant_missing_docs_april.txt']
		}
	},
	{
		keywords: [
			'lumina',
			'missing',
			'lipsa',
			'lipseste',
			'invoice',
			'factura',
			'lumina design'
		],
		result: {
			answer:
				'The Lumina Design invoice (LD 0041, 3,046.40 RON) is missing the **internal purchase order reference**. The supplier did not include it on the invoice. You need to confirm the PO number with the supplier or internally, then forward the document to the accountant.',
			sources: ['invoice_lumina_design_2026_0041.pdf']
		}
	},
	{
		keywords: ['payment terms', 'termeni plata', 'termene de plata', 'plata lumina', 'lumina payment'],
		result: {
			answer:
				'According to the Lumina Design supplier contract (no. 12/15.03.2026), invoices must be paid within **14 calendar days** from the invoice date. Late payments incur a penalty of **0.05% per day** on the outstanding amount after 10 days. The contract is valid until 31.12.2026.',
			sources: ['contract_supplier_lumina_design.txt']
		}
	},
	{
		keywords: ['draft reply', 'apartment', 'apartament', 'bucuresti', 'bucharest', 'draft a reply', 'raspuns'],
		result: {
			answer:
				'To draft a reply for the apartment client (Radu Enache), go to **AI Inbox** and open the document **email_client_apartament_bucuresti.txt**. A Draft Reply panel is available there with a pre-prepared Romanian reply. You can review it, edit it locally, and approve it — no email will be sent automatically.',
			sources: ['email_client_apartament_bucuresti.txt']
		}
	},
	{
		keywords: ['showroom', 'pitesti', 'pitești', 'mention', 'mentioneaza'],
		result: {
			answer:
				'Three documents mention Showroom Pitești. **contract_client_showroom_renovation.txt** is the main contract (220 sqm, 3 phases, deadline 30.06.2026). **email_client_showroom_pitesti.txt** is a client status request — note that the client references 15 May but the contract says 30 May for phase 1. **email_accountant_missing_docs_april.txt** also mentions the signed contract as one of the four missing documents.',
			sources: [
				'contract_client_showroom_renovation.txt',
				'email_client_showroom_pitesti.txt',
				'email_accountant_missing_docs_april.txt'
			]
		}
	},
	{
		keywords: ['send', 'trimite', 'contabil', 'accountant', 'before 10', 'inainte de 10', '10 may', '10 mai'],
		result: {
			answer:
				'Before 10 May, the accountant needs four items: (1) **invoice_lumina_design_2026_0041.pdf** — the LED panels invoice, (2) **invoice_printstudio_2026_0098.pdf** — payment confirmation for PrintStudio, (3) **contract_client_showroom_renovation.txt** — the signed Showroom Pitești contract, and (4) a written explanation of who approved the SoftCloud subscription (linked to **invoice_softcloud_2026_0520.pdf**).',
			sources: [
				'email_accountant_missing_docs_april.txt',
				'invoice_lumina_design_2026_0041.pdf',
				'invoice_printstudio_2026_0098.pdf',
				'contract_client_showroom_renovation.txt',
				'invoice_softcloud_2026_0520.pdf'
			]
		}
	},
	{
		keywords: ['penalty', 'penalitate', 'penalitati', 'penalties', 'contract', 'contracte'],
		result: {
			answer:
				'Yes — two contracts include payment penalty clauses. **contract_client_showroom_renovation.txt** (client-side) has a penalty of **0.1% per day** for delays past 30 June 2026. **contract_supplier_lumina_design.txt** (supplier-side) has a penalty of **0.05% per day** for late payments after 10 days. The client-side penalty is twice as strict, which means any project delay hits Atelier Nova asymmetrically.',
			sources: ['contract_client_showroom_renovation.txt', 'contract_supplier_lumina_design.txt']
		}
	}
];

export function matchQuestion(input: string): QAResult | null {
	const normalized = input
		.toLowerCase()
		.normalize('NFD')
		.replace(/[̀-ͯ]/g, '');

	for (const pair of QA_PAIRS) {
		for (const keyword of pair.keywords) {
			const normKeyword = keyword
				.toLowerCase()
				.normalize('NFD')
				.replace(/[̀-ͯ]/g, '');
			if (normalized.includes(normKeyword)) {
				return pair.result;
			}
		}
	}

	return null;
}

export const EXAMPLE_QUESTIONS = [
	'Which invoices are urgent this week?',
	'What documents did the accountant request?',
	'What is missing from the Lumina Design invoice?',
	'What are the payment terms with Lumina Design?',
	'Draft a reply to the apartment client.',
	'Which documents mention Showroom Pitești?',
	'What should I send to the accountant before 10 May?',
	'Are there any contracts with payment penalties?'
];
