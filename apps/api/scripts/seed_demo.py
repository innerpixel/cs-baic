"""Seed the full 7-document demo set into the API.

Documents:
  - 5 supplier invoices
  - 1 supplier contract
  - 1 accountant request email
"""
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import json

API_BASE = "http://localhost:8000"

DOCUMENTS = [
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
2. Cablu alimentare și accesorii montaj, 1 set, 340 RON

Subtotal: 2.560 RON
TVA: 486,40 RON
Total de plată: 3.046,40 RON
Scadență: 12.05.2026
IBAN: RO00BANK0000000000000001

Mențiune: Comanda internă nu este trecută pe factură.""",
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

Produse și servicii:
1. Rafturi personalizate model Industrial Slim, 4 module, 720 RON/buc = 2.880 RON
2. Montaj și fixare la locație, 1 serviciu = 280 RON

Subtotal: 3.160 RON (TVA inclus 504 RON)
Total de plată: 3.160,00 RON
Scadență: 21.05.2026

Notă: Livrarea a fost confirmată telefonic pe 29.04.2026. Procesul-verbal de recepție nu a fost semnat.""",
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
CUI Client: RO00000002

Produse:
1. Cataloage produs format A4, 200 exemplare, 2,20 RON/buc = 440 RON
2. Cărți de vizită premium, 500 buc, 0,60 RON/buc = 300 RON
3. Design grafic și pregătire tipărire, 1 serviciu = 108 RON

Total: 848,00 RON (TVA inclus)
Mențiune: Factura a fost achitată prin ordin bancar pe 02.05.2026.
Confirmarea plății nu a fost transmisă contabilului.""",
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
CUI Client: RO00000002

Servicii livrare aprilie 2026:
1. Livrare pachet mobilier mic (01.04.2026) — 85 RON
2. Livrare mostre materiale textile (10.04.2026) — 95 RON
3. Livrare comandă client Ionescu (18.04.2026) — 145 RON [DISPUTAT]
4. Livrare accesorii LED (24.04.2026) — 116 RON

Total: 441,00 RON (TVA inclus)
Scadență: 15.05.2026

Notă internă: Clientul Ionescu a reclamat că pachetul din 18.04 era incomplet. Situația nu este clarificată.""",
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
CUI Client: RO00000002

Servicii:
1. Abonament cloud hosting Standard — mai 2026: 150 RON
2. Serviciu backup automat zilnic — mai 2026: 70 RON

Total: 220,00 RON (TVA inclus)
Scadență: 18.05.2026

Mențiune: Nu există în evidențele interne o aprobare scrisă sau un e-mail de confirmare pentru acest abonament. Contabilul a solicitat clarificări.""",
    },
    {
        "filename": "contract_supplier_lumina_design.txt",
        "type": "contract",
        "text": """\
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
    },
    {
        "filename": "email_accountant_missing_docs_april.txt",
        "type": "accountant_request",
        "text": """\
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
    },
]


def upload(doc: dict) -> str:
    boundary = "---SeederBoundary"
    lines = []
    for field in ("text", "filename", "type"):
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{field}"')
        lines.append("")
        lines.append(doc[field])
    lines.append(f"--{boundary}--")
    body = "\r\n".join(lines).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE}/api/documents",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["id"]


def poll(doc_id: str, max_wait: int = 90) -> dict | None:
    for _ in range(max_wait // 2):
        req = urllib.request.Request(f"{API_BASE}/api/documents/{doc_id}")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        if data["status"] in ("done", "failed", "not_supported_yet"):
            return data
        time.sleep(2)
    return None


def main():
    print(f"Seeding {len(DOCUMENTS)} documents into {API_BASE}…\n")
    for doc in DOCUMENTS:
        print(f"Uploading {doc['filename']} ({doc['type']}) ...", end=" ", flush=True)
        try:
            doc_id = upload(doc)
        except urllib.error.URLError as e:
            print(f"FAILED (upload error): {e}")
            sys.exit(1)
        print(f"id={doc_id}", end=" ", flush=True)

        result = poll(doc_id)
        if result is None:
            print("TIMEOUT — analysis did not complete in 90s")
            continue

        analysis = result.get("analysis")
        status = result["status"]
        if analysis:
            summary = (analysis.get("summary") or "")[:60]
            urgency = analysis.get("urgency") or "—"
            dtype = analysis.get("detected_type") or "—"
            print(f"OK · status={status} · urgency={urgency} · detected={dtype} · summary={summary!r}")
        else:
            print(f"status={status}")

    print("\nDone. Run GET /api/documents to verify 7 rows.")


if __name__ == "__main__":
    main()
