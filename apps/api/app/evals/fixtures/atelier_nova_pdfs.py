"""Eval fixtures sourced from the slice-7 Atelier Nova SRL PDF set.

These complement the text-based fixtures in the parent fixtures.py.
Input text here mirrors the content of the authored PDFs so the analyzer
pipeline can be exercised without a live database.
"""

FIXTURES_NOVA_PDFS: dict[str, dict] = {
    # ── supplier invoice: Lumina Design, LED panels (series 2) ──────────────
    "invoice_lumina_v2_pdf": {
        "input_text": """\
FACTURĂ FISCALĂ
Seria LD Nr. 0042
Data emiterii: 15.04.2026

FURNIZOR
Lumina Design SRL
CUI: ROƐ1234567
Reg. Com.: J03/Ɛ456/2018
Adresă: Str. Luminii nr. 14, Pitești, Argeș
IBAN: ROƐƐBANK0000000001

CLIENT
Atelier Nova SRL
CUI: ROƐ9876543
Adresă: Str. Victoriei nr. 8, Pitești, Argeș

Produse / Servicii:
Nr.  Denumire                              Cant.  UM   Preț/UM     Total
1    Spoturi LED încastrate, 6W, alb rece  24     buc  45,00 RON   1.080,00 RON
2    Transformatoare 60W compatibile       6      buc  78,00 RON   468,00 RON
3    Cablu alimentare 2m + clemă           24     buc  12,50 RON   300,00 RON

Subtotal (fără TVA):  1.848,00 RON
TVA 19%:              351,12 RON
TOTAL DE PLATĂ:       2.199,12 RON

Scadență: 29.04.2026
IBAN plată: ROƐƐBANK0000000001

Menționăm că această factură nu include numărul de comandă intern Atelier Nova.""",
        "doc_type": "supplier_invoice",
        "expected": {
            "invoice_extractor": {
                "supplier_name": "Lumina Design SRL",
                "total_amount": "2199.12",
                "currency": "RON",
                "due_date": "29.04.2026",
                "missing_fields_contains": ["internal purchase order reference"],
            },
            "summarizer": {
                "short_summary_contains": ["Lumina Design", "2"],
                "urgency": "high",
            },
            "classifier": {
                "document_type": "supplier_invoice",
                "language": "ro",
            },
        },
    },

    # ── contract: Mobilier Concept SRL collaboration ─────────────────────────
    "contract_mobilier_pdf": {
        "input_text": """\
CONTRACT DE COLABORARE Nr. 07/2026
Încheiat la data de 01.03.2026

PĂRȚI CONTRACTANTE

FURNIZOR: Mobilier Concept SRL
CUI: ROƐ2345678
Reg. Com.: J03/Ɛ789/2015
Reprezentat prin: Gheorghe Ionescu — Administrator

BENEFICIAR: Atelier Nova SRL
CUI: ROƐ9876543
Reprezentat prin: Irina Florescu — Administrator

OBIECT
Furnizarea de mobilier la comandă și mobilier de serie pentru proiectele de design interior
ale Beneficiarului, conform specificațiilor transmise pentru fiecare comandă.

TERMENE DE LIVRARE
Art. 3.1 — Mobilierul la comandă se livrează în termen de 21 de zile lucrătoare de la
confirmarea scrisă a comenzii.
Art. 3.2 — Mobilierul de serie disponibil în stoc se livrează în termen de 5 zile lucrătoare.

CONDIȚII DE PLATĂ
Art. 4.1 — Beneficiarul achită 30% din valoarea comenzii la confirmare.
Art. 4.2 — Soldul de 70% se achită în termen de 10 zile calendaristice de la livrare.
Art. 4.3 — Întârzierile la plată atrag penalități de 0,08% pe zi din suma restantă.

GARANȚIE
Art. 5.1 — Furnizorul acordă garanție 24 de luni pentru mobilierul la comandă.

DURATĂ ȘI REZILIERE
Art. 6.1 — Contractul este valabil până la 31.12.2026.
Art. 6.2 — Oricare parte poate rezilia cu notificare scrisă cu 30 de zile înainte.
Art. 6.3 — Rezilierea fără notificare prealabilă atrage penalități echivalente cu 15%
din valoarea comenzilor în derulare.

SEMNĂTURI
Furnizor: Gheorghe Ionescu          Beneficiar: Irina Florescu
Data: 01.03.2026                    Data: 01.03.2026""",
        "doc_type": "contract",
        "expected": {
            "contract_reviewer": {
                "payment_terms_contains": ["10"],
                "penalties_contains": [["0,08", "0.08"], "30"],
                "termination_terms_nonempty": True,
                "risk_flags_nonempty": True,
            },
            "summarizer": {
                "short_summary_contains": ["Mobilier Concept", "10"],
                "urgency_not_unknown": True,
            },
            "classifier": {
                "document_type": "contract",
                "language": "ro",
            },
        },
    },

    # ── client request: Aurora Construct — showroom design ───────────────────
    "client_request_aurora_pdf": {
        "input_text": """\
Aurora Construct SRL
CUI: ROƐ3456789
Str. Industriilor nr. 22, București

Către: Atelier Nova SRL
Data: 05.04.2026

Subiect: Cerere ofertă amenajare showroom industrial

Stimată doamnă Florescu,

Dorim să amenajăm un showroom de prezentare pentru produsele noastre de construcții,
cu o suprafață totală de 180 mp în București, sector 2. Spațiul va servi atât ca zonă
de expunere cât și ca spațiu de întâlniri cu clienții.

Cerințe principale:
— Concept vizual care să reflecte valorile brandului (industrial, solid, modern)
— Zone de expunere produse cu iluminat tehnic de calitate
— Birou de recepție și spațiu de așteptare (minim 20 mp)
— Sală de ședințe pentru maxim 12 persoane
— Posibilitate de reconfigurare rapidă a zonei de expunere

Ne interesează să primiți o ofertă de consultanță și design interior care să includă:
— Concept și vizualizare 3D
— Listă de materiale și furnizori recomandați
— Estimare costuri amenajare
— Plan de implementare pe etape

Am dori să finalizăm designul până la 30 mai 2026 pentru a demara lucrările în iunie.

Vă rugăm să ne confirmați disponibilitatea și să ne transmiteți oferta în termen de 10 zile.

Cu respect,
Andrei Marinescu
Director General, Aurora Construct SRL
Tel: +40 7ƐƐ ƐƐƐ ƐƐƐ
Email: andrei.marinescu@aurora-construct.ro""",
        "doc_type": "client_request",
        "expected": {
            "summarizer": {
                "short_summary_contains": ["Aurora", "180"],
                "urgency_not_critical": True,
            },
            "classifier": {
                "document_type": "client_request",
                "language": "ro",
            },
        },
    },
}
