"""Eval fixtures from §23.3 of the project control pack.

Each fixture has:
  input_text: str
  doc_type: str
  expected: dict[analyzer_name, expected_output_dict]

Expected outputs define which keys to check and their expected values.
None values mean "must be present and non-null" but any value is acceptable.
"""

FIXTURES: dict[str, dict] = {
    "invoice_lumina": {
        "input_text": """\
Factura seria LD nr. 0041
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

Mențiune: Comanda internă nu este trecută pe factură.""",
        "doc_type": "supplier_invoice",
        "expected": {
            "invoice_extractor": {
                "supplier_name": "Lumina Design SRL",
                "supplier_cui": "RO00000001",
                "invoice_number": "LD 0041",
                "invoice_date": "28.04.2026",
                "due_date": "12.05.2026",
                "total_amount": "3046.40",
                "currency": "RON",
                "vat_amount": "486.40",
                "missing_fields_contains": ["internal purchase order reference"],
            },
            "summarizer": {
                "short_summary_contains": ["Lumina Design", "3"],
                "urgency": "high",
            },
            "classifier": {
                "document_type": "supplier_invoice",
                "language": "ro",
            },
        },
    },

    "accountant_email": {
        "input_text": """\
Subiect: Documente lipsă pentru luna aprilie

Bună, Irina,

Pentru închiderea lunii aprilie am nevoie de următoarele documente:

1. Factura de la Lumina Design SRL pentru panourile LED.
2. Confirmarea plății către PrintStudio pentru materialele promoționale.
3. Contractul semnat cu clientul pentru proiectul Showroom Pitești.
4. Explicație pentru factura SoftCloud, deoarece nu apare persoana care a aprobat abonamentul.

Te rog să mi le trimiți până pe 10 mai ca să putem finaliza raportarea la timp.

Mulțumesc,
Mihai""",
        "doc_type": "accountant_request",
        "expected": {
            "summarizer": {
                "short_summary_contains": ["accountant", "four", "4", "mai", "May", "10"],
                "urgency": "high",
            },
            "classifier": {
                "document_type": "accountant_request",
                "language": "ro",
            },
        },
    },

    "client_apartament_email": {
        "input_text": """\
Subiect: Cerere ofertă amenajare apartament 3 camere

Bună ziua,

Am găsit portofoliul Atelier Nova și am dori o ofertă pentru amenajarea unui apartament de 3 camere în București, aproximativ 78 mp.

Ne interesează:
- consultanță design interior
- propunere cromatică
- recomandări mobilier
- eventual coordonare furnizori

Am vrea să începem în luna iunie. Ne puteți spune ce informații aveți nevoie și care este un cost estimativ?

Mulțumesc,
Radu Enache""",
        "doc_type": "client_request",
        "expected": {
            "summarizer": {
                "short_summary_contains": ["apartment", "apartament", "Bucharest", "București", "78"],
                "urgency_not_critical": True,  # should be low or medium, not high
            },
            "classifier": {
                "document_type": "client_request",
                "language": "ro",
            },
        },
    },

    "contract_lumina": {
        "input_text": """\
Contract de colaborare nr. 12 din 15.03.2026

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
Oricare parte poate denunța contractul cu notificare scrisă transmisă cu 30 de zile înainte.""",
        "doc_type": "contract",
        "expected": {
            "contract_reviewer": {
                "payment_terms_contains": ["14"],
                "penalties_contains": ["0.05", "10"],
                "termination_terms_nonempty": True,
                "risk_flags_nonempty": True,
            },
            "summarizer": {
                "short_summary_contains": ["Lumina Design", "14"],
                "urgency_not_unknown": True,
            },
            "classifier": {
                "document_type": "contract",
                "language": "ro",
            },
        },
    },
}
