"""Generate the 8 Atelier Nova SRL demo documents as PDF files.

Output: apps/api/scripts/demo_pdfs/
Run:    uv run --with fpdf2 python scripts/generate_demo_pdfs.py
"""
from pathlib import Path
from fpdf import FPDF

OUT_DIR = Path(__file__).parent / "demo_pdfs"

DOCUMENTS = [
    {
        "filename": "invoice_lumina_design_2026_0041.pdf",
        "title": "Factura LD nr. 0041 — Lumina Design SRL",
        "text": """\
Factura seria LD nr. 0041
Data emiterii: 28.04.2026
Furnizor: Lumina Design SRL
CUI: RO00000001
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse:
1. Panouri LED decorative model Aurora, 12 buc, 185 RON/buc
2. Cablu alimentare si accesorii montaj, 1 set, 340 RON

Subtotal: 2.560 RON
TVA: 486,40 RON
Total de plata: 3.046,40 RON
Scadenta: 12.05.2026
IBAN: RO00BANK0000000000000001

Mentiune: Comanda interna nu este trecuta pe factura.""",
    },
    {
        "filename": "invoice_mobila_artisan_2026_0187.pdf",
        "title": "Factura MA nr. 0187 — Mobila Artisan SRL",
        "text": """\
Factura seria MA nr. 0187
Data emiterii: 30.04.2026
Furnizor: Mobila Artisan SRL
CUI: RO00000003
IBAN: RO00BANK0000000000000003
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse si servicii:
1. Rafturi personalizate model Industrial Slim, 4 module, 720 RON/buc = 2.880 RON
2. Montaj si fixare la locatie, 1 serviciu = 280 RON

Subtotal: 3.160 RON (TVA inclus 504 RON)
Total de plata: 3.160,00 RON
Scadenta: 21.05.2026

Nota: Livrarea a fost confirmata telefonic pe 29.04.2026.
Procesul-verbal de receptie nu a fost semnat.""",
    },
    {
        "filename": "invoice_printstudio_2026_0098.pdf",
        "title": "Factura PS nr. 0098 — PrintStudio Media SRL",
        "text": """\
Factura seria PS nr. 0098
Data emiterii: 25.04.2026
Furnizor: PrintStudio Media SRL
CUI: RO00000004
Client: Atelier Nova SRL
CUI Client: RO00000002

Produse:
1. Cataloage produs format A4, 200 exemplare, 2,20 RON/buc = 440 RON
2. Carti de vizita premium, 500 buc, 0,60 RON/buc = 300 RON
3. Design grafic si pregatire tiparire, 1 serviciu = 108 RON

Total: 848,00 RON (TVA inclus)
Mentiune: Factura a fost achitata prin ordin bancar pe 02.05.2026.
Confirmarea platii nu a fost transmisa contabilului.""",
    },
    {
        "filename": "invoice_curier_rapid_2026_1142.pdf",
        "title": "Factura CR nr. 1142 — Curier Rapid Express SRL",
        "text": """\
Factura seria CR nr. 1142
Data emiterii: 30.04.2026
Furnizor: Curier Rapid Express SRL
CUI: RO00000005
Client: Atelier Nova SRL
CUI Client: RO00000002

Servicii livrare aprilie 2026:
1. Livrare pachet mobilier mic (01.04.2026) — 85 RON
2. Livrare mostre materiale textile (10.04.2026) — 95 RON
3. Livrare comanda client Ionescu (18.04.2026) — 145 RON [DISPUTAT]
4. Livrare accesorii LED (24.04.2026) — 116 RON

Total: 441,00 RON (TVA inclus)
Scadenta: 15.05.2026

Nota interna: Clientul Ionescu a reclamat ca pachetul din 18.04 era incomplet.
Situatia nu este clarificata.""",
    },
    {
        "filename": "invoice_softcloud_2026_0520.pdf",
        "title": "Factura SC nr. 0520 — SoftCloud Solutions SRL",
        "text": """\
Factura seria SC nr. 0520
Data emiterii: 01.05.2026
Furnizor: SoftCloud Solutions SRL
CUI: RO00000006
Client: Atelier Nova SRL
CUI Client: RO00000002

Servicii:
1. Abonament cloud hosting Standard — mai 2026: 150 RON
2. Serviciu backup automat zilnic — mai 2026: 70 RON

Total: 220,00 RON (TVA inclus)
Scadenta: 18.05.2026

Mentiune: Nu exista in evidentele interne o aprobare scrisa sau un e-mail
de confirmare pentru acest abonament.
Contabilul a solicitat clarificari.""",
    },
    {
        "filename": "contract_supplier_lumina_design.pdf",
        "title": "Contract de colaborare nr. 12 — Lumina Design SRL",
        "text": """\
Contract de colaborare nr. 12 din 15.03.2026

Parti:
Lumina Design SRL, in calitate de furnizor
Atelier Nova SRL, in calitate de beneficiar

Obiect:
Furnizarea de corpuri de iluminat decorative, panouri LED si accesorii
pentru proiectele Atelier Nova.

Termen de livrare:
Furnizorul livreaza produsele in termen de 7 zile lucratoare de la
confirmarea comenzii.

Plata:
Beneficiarul achita facturile in termen de 14 zile calendaristice de la
data emiterii facturii.

Penalitati:
Pentru intarzieri la plata mai mari de 10 zile, se pot aplica penalitati
de 0,05% pe zi din suma restanta.

Durata:
Contractul este valabil pana la 31.12.2026 si se poate prelungi prin
acord scris.

Incetare:
Oricare parte poate denunta contractul cu notificare scrisa transmisa cu
30 de zile inainte.""",
    },
    {
        "filename": "email_client_apartament_bucuresti.pdf",
        "title": "Cerere oferta amenajare apartament — Radu Enache",
        "text": """\
Subiect: Cerere oferta amenajare apartament 3 camere

Buna ziua,

Am gasit portofoliul Atelier Nova si am dori o oferta pentru amenajarea
unui apartament de 3 camere in Bucuresti, aproximativ 78 mp.

Ne intereseaza:
- consultanta design interior
- propunere cromatica
- recomandari mobilier
- eventual coordonare furnizori

Am vrea sa incepem in luna iunie. Ne puteti spune ce informatii aveti
nevoie si care este un cost estimativ?

Multumesc,
Radu Enache""",
    },
    {
        "filename": "email_accountant_missing_docs_april.pdf",
        "title": "Documente lipsa pentru luna aprilie — Mihai (contabil)",
        "text": """\
Subiect: Documente lipsa pentru luna aprilie

Buna, Irina,

Pentru inchiderea lunii aprilie am nevoie de urmatoarele documente:

1. Factura de la Lumina Design SRL pentru panourile LED.
2. Confirmarea platii catre PrintStudio pentru materialele promotionale.
3. Contractul semnat cu clientul pentru proiectul Showroom Pitesti.
4. Explicatie pentru factura SoftCloud, deoarece nu apare persoana care
   a aprobat abonamentul.

Te rog sa mi le trimiti pana pe 10 mai ca sa putem finaliza raportarea
la timp.

Multumesc,
Mihai""",
    },
]


FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def make_pdf(doc: dict) -> None:
    pdf = FPDF()
    pdf.add_font("DejaVu", style="", fname=FONT_REGULAR)
    pdf.add_font("DejaVu", style="B", fname=FONT_BOLD)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    w = pdf.epw

    # Title
    pdf.set_font("DejaVu", style="B", size=13)
    pdf.multi_cell(w, 8, doc["title"])
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(180, 180, 180)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.l_margin + w, y)
    pdf.ln(6)

    # Body — write entire text in one call so multi_cell handles line breaks
    pdf.set_font("DejaVu", size=10)
    pdf.multi_cell(w, 6, doc["text"])

    out = OUT_DIR / doc["filename"]
    pdf.output(str(out))
    print(f"  {doc['filename']}")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Writing {len(DOCUMENTS)} PDFs to {OUT_DIR}/\n")
    for doc in DOCUMENTS:
        make_pdf(doc)
    print(f"\nDone. Upload them via /app/inbox.")


if __name__ == "__main__":
    main()
