"""Seed demo data into the API database.

Usage:
    cd apps/api
    uv run python scripts/seed_demo.py [--company atelier-nova] [--include-dev-source]

Modes:
    --company atelier-nova  (default) generates 18 Atelier Nova PDFs and ingests them.
    --include-dev-source    additionally seeds the 8 legacy text docs as source=dev_source.
"""
import argparse
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.services.analysis import run_analysis
from app.services.upload_intake import ingest_pdf


YAML_DIR = Path(__file__).parent / "demo_content" / "atelier_nova"
PDF_DIR = Path(__file__).parent.parent / "var" / "demo_pdfs" / "atelier_nova"

# 8 legacy text docs → seeded as source=dev_source
DEV_SOURCE_DOCS = [
    {
        "filename": "invoice_lumina_design_2026_0041.txt",
        "type": "supplier_invoice",
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
        "filename": "invoice_mobila_artisan_2026_0187.txt",
        "type": "supplier_invoice",
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
Scadenta: 21.05.2026""",
    },
    {
        "filename": "invoice_printstudio_2026_0098.txt",
        "type": "supplier_invoice",
        "text": """\
Factura seria PS nr. 0098
Data emiterii: 25.04.2026
Furnizor: PrintStudio Media SRL
CUI: RO00000004
Client: Atelier Nova SRL

Produse:
1. Cataloage produs format A4, 200 exemplare, 2,20 RON/buc = 440 RON
2. Carti de vizita premium, 500 buc, 0,60 RON/buc = 300 RON
3. Design grafic si pregatire tiparire, 1 serviciu = 108 RON

Total: 848,00 RON (TVA inclus)""",
    },
    {
        "filename": "invoice_curier_rapid_2026_1142.txt",
        "type": "supplier_invoice",
        "text": """\
Factura seria CR nr. 1142
Data emiterii: 30.04.2026
Furnizor: Curier Rapid Express SRL
CUI: RO00000005
Client: Atelier Nova SRL

Servicii livrare aprilie 2026:
1. Livrare pachet mobilier mic (01.04.2026) — 85 RON
2. Livrare mostre materiale textile (10.04.2026) — 95 RON
3. Livrare comanda client Ionescu (18.04.2026) — 145 RON [DISPUTAT]
4. Livrare accesorii LED (24.04.2026) — 116 RON

Total: 441,00 RON (TVA inclus)
Scadenta: 15.05.2026""",
    },
    {
        "filename": "invoice_softcloud_2026_0520.txt",
        "type": "supplier_invoice",
        "text": """\
Factura seria SC nr. 0520
Data emiterii: 01.05.2026
Furnizor: SoftCloud Solutions SRL
CUI: RO00000006
Client: Atelier Nova SRL

Servicii:
1. Abonament cloud hosting Standard — mai 2026: 150 RON
2. Serviciu backup automat zilnic — mai 2026: 70 RON

Total: 220,00 RON (TVA inclus)
Scadenta: 18.05.2026""",
    },
    {
        "filename": "contract_supplier_lumina_design.txt",
        "type": "contract",
        "text": """\
Contract de colaborare nr. 12 din 15.03.2026

Parti:
Lumina Design SRL, in calitate de furnizor
Atelier Nova SRL, in calitate de beneficiar

Obiect:
Furnizarea de corpuri de iluminat decorative, panouri LED si accesorii.

Termen de livrare:
Furnizorul livreaza produsele in termen de 7 zile lucratoare de la confirmarea comenzii.

Plata:
Beneficiarul achita facturile in termen de 14 zile calendaristice de la data emiterii.

Penalitati:
Pentru intarzieri la plata mai mari de 10 zile, penalitati de 0,05% pe zi.

Durata: valabil pana la 31.12.2026.""",
    },
    {
        "filename": "email_client_apartament_bucuresti.txt",
        "type": "client_request",
        "text": """\
Subiect: Cerere oferta amenajare apartament 3 camere

Buna ziua,

Am gasit portofoliul Atelier Nova si am dori o oferta pentru amenajarea unui apartament
de 3 camere in Bucuresti, aproximativ 78 mp.

Ne intereseaza: consultanta design interior, propunere cromatica, recomandari mobilier,
eventual coordonare furnizori.

Am vrea sa incepem in luna iunie.

Multumesc,
Radu Enache""",
    },
    {
        "filename": "email_accountant_missing_docs_april.txt",
        "type": "accountant_request",
        "text": """\
Subiect: Documente lipsa pentru luna aprilie

Buna, Irina,

Pentru inchiderea lunii aprilie am nevoie de:
1. Factura de la Lumina Design SRL pentru panourile LED.
2. Confirmarea platii catre PrintStudio.
3. Contractul semnat cu clientul pentru proiectul Showroom Pitesti.
4. Explicatie pentru factura SoftCloud (persoana care a aprobat abonamentul).

Te rog sa mi le trimiti pana pe 10 mai.

Multumesc,
Mihai""",
    },
]


def _load_yaml_categories() -> dict[str, str]:
    cats = {}
    for yf in YAML_DIR.glob("*.yaml"):
        y = yaml.safe_load(yf.read_text(encoding="utf-8"))
        cats[y["filename"]] = y["category"]
    return cats


def seed_atelier_nova(db) -> int:
    from scripts.generate_demo_pdfs import generate_all
    print("Generating Atelier Nova PDFs…")
    results = generate_all()
    failed = [r for r in results if not r["ok"]]
    if failed:
        print(f"WARNING: {len(failed)} PDFs failed to generate: {[r['filename'] for r in failed]}")

    categories = _load_yaml_categories()
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print("ERROR: no PDFs found in var/demo_pdfs/atelier_nova/ — generation may have failed")
        return 0

    count = 0
    for pdf_path in pdf_files:
        pdf_bytes = pdf_path.read_bytes()
        category = categories.get(pdf_path.name, "unknown")
        print(f"  Ingesting {pdf_path.name} ({category}) …", end=" ", flush=True)
        doc_id = ingest_pdf(
            filename=pdf_path.name,
            pdf_bytes=pdf_bytes,
            db=db,
            doc_type=category,
            source="public",
        )
        run_analysis(doc_id, db)
        doc = db.get(__import__("app.db.models", fromlist=["Document"]).Document, doc_id)
        print(f"status={doc.status}")
        count += 1

    return count


def seed_dev_source(db) -> int:
    import uuid as _uuid
    from app.db.models import AuditEvent, Document
    count = 0
    for doc_spec in DEV_SOURCE_DOCS:
        doc_id = _uuid.uuid4()
        doc = Document(
            id=doc_id,
            filename=doc_spec["filename"],
            type=doc_spec["type"],
            raw_text=doc_spec["text"],
            status="queued",
            source="dev_source",
        )
        db.add(doc)
        db.add(AuditEvent(
            document_id=doc_id,
            event_type="uploaded",
            event_data={"filename": doc_spec["filename"], "source": "dev_source"},
        ))
        db.commit()
        print(f"  Ingesting {doc_spec['filename']} (dev_source) …", end=" ", flush=True)
        run_analysis(doc_id, db)
        doc = db.get(Document, doc_id)
        print(f"status={doc.status}")
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="Seed NovAI Desk demo data")
    parser.add_argument("--company", default="atelier-nova", choices=["atelier-nova"],
                        help="Demo company to seed (default: atelier-nova)")
    parser.add_argument("--include-dev-source", action="store_true",
                        help="Also seed the 8 legacy text docs as source=dev_source")
    args = parser.parse_args()

    with SessionLocal() as db:
        if args.company == "atelier-nova":
            n = seed_atelier_nova(db)
            print(f"\nAtelier Nova: {n} PDFs seeded.")

        if args.include_dev_source:
            n = seed_dev_source(db)
            print(f"Dev source: {n} text docs seeded.")

    print("\nDone. Run GET /api/documents to verify rows.")


if __name__ == "__main__":
    main()
