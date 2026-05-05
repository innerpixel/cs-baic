"""Seed the 5 supplier invoices from apps/web/src/lib/data/inbox.ts into the API."""
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import json

API_BASE = "http://localhost:8000"

INVOICES = [
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
]


def upload(invoice: dict) -> str:
    boundary = "---SeederBoundary"
    lines = []
    for field in ("text", "filename", "type"):
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{field}"')
        lines.append("")
        lines.append(invoice[field])
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


def poll(doc_id: str, max_wait: int = 60) -> dict | None:
    for _ in range(max_wait // 2):
        req = urllib.request.Request(f"{API_BASE}/api/documents/{doc_id}")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        if data["status"] in ("done", "failed"):
            return data
        time.sleep(2)
    return None


def main():
    for inv in INVOICES:
        print(f"Uploading {inv['filename']} ...", end=" ", flush=True)
        try:
            doc_id = upload(inv)
        except urllib.error.URLError as e:
            print(f"FAILED (upload error): {e}")
            sys.exit(1)
        print(f"id={doc_id}", end=" ", flush=True)

        result = poll(doc_id)
        if result is None:
            print("TIMEOUT — analysis did not complete in 60s")
            continue

        analysis = result.get("analysis")
        if analysis and analysis.get("fields"):
            fields = analysis["fields"]
            print(
                f"OK · supplier={fields.get('supplier_name')} · "
                f"invoice={fields.get('invoice_number')} · "
                f"total={fields.get('total_amount')} {fields.get('currency')}"
            )
        else:
            print(f"status={result['status']} (analysis={analysis})")


if __name__ == "__main__":
    main()
