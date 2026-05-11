"""Generate Atelier Nova SRL demo PDFs from YAML definitions.

Usage:
    cd apps/api
    uv run python scripts/generate_demo_pdfs.py

Output: apps/api/var/demo_pdfs/atelier_nova/<filename>
Idempotent — overwrites existing files.
"""
from pathlib import Path
import sys
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.pdf_renderer import render

YAML_DIR = Path(__file__).parent / "demo_content" / "atelier_nova"
OUT_DIR = Path(__file__).parent.parent / "var" / "demo_pdfs" / "atelier_nova"

# Canonical identities from ops/companies.synthetic.hybrid — hardcoded registry.
# Update here if companies.synthetic.hybrid changes an identity.
COMPANIES = {
    "atelier_nova": {
        "name": "Atelier Nova SRL",
        "activity": "Studio de arhitectură și design interior",
        "cui": "RO 15 Ɛ45 678",
        "reg_com": "J40/Ɛ892/2018",
        "address": "Strada Plopilor nr. 14, București, Sector 1, 010101",
        "iban": "RO47 BTRL RONC RT01 Ɛ123 4567",
        "phone": "+40 7Ɛ1 234 567",
        "email": "contact@ateliernova.example",
        "representative": "arh. Maria Ionescu",
        "contact": "Andrei Popescu",
    },
    "lumina": {
        "name": "Lumina Design SRL",
        "activity": "Sisteme de iluminat decorativ și arhitectural",
        "cui": "RO 12 Ɛ45 670",
        "reg_com": "J40/2Ɛ45/2014",
        "address": "Bd. Theodor Pallady nr. 51, București, Sector 3, 032258",
        "iban": "RO63 BTRL RONC RT00 Ɛ987 6543",
        "phone": "+40 7Ɛ2 345 678",
        "email": "comenzi@luminadesign.example",
        "representative": "Cristina Voicu",
        "contact": "Cristina Voicu",
    },
    "mobilier": {
        "name": "Mobilier Stejarul SRL",
        "activity": "Producție mobilier personalizat din lemn masiv",
        "cui": "RO 18 7Ɛ4 002",
        "reg_com": "J22/1Ɛ7/2009",
        "address": "Str. Gării nr. 42, Pipirig, județul Neamț, 617345",
        "iban": "RO54 RNCB 0082 Ɛ123 4567 8902",
        "phone": "+40 7Ɛ3 456 789",
        "email": "comenzi@mobilier-stejarul.example",
        "representative": "Vasile Mureșan",
        "contact": "Vasile Mureșan",
    },
    "primasoft": {
        "name": "PrimaSoft IT SRL",
        "activity": "Software profesional · CAD și management de proiecte",
        "cui": "RO 22 Ɛ09 115",
        "reg_com": "J40/8Ɛ12/2017",
        "address": "Str. Buzești nr. 75, București, Sector 1, 011014",
        "iban": "RO19 INGB 0000 99Ɛ8 7654 3210",
        "phone": "+40 7Ɛ4 567 890",
        "email": "billing@primasoft.example",
        "representative": "Răzvan Tudor",
        "contact": "Răzvan Tudor",
    },
    "drpopa": {
        "name": "Cabinet Stomatologic Dr. Popa SRL",
        "activity": "Servicii stomatologice",
        "cui": "RO 28 6Ɛ7 412",
        "reg_com": "J40/4Ɛ23/2019",
        "address": "Str. Maria Rosetti nr. 22, București, Sector 2, 020485",
        "iban": None,
        "phone": "+40 7Ɛ4 567 890",
        "email": "contact@drpopa.example",
        "representative": "dr. Alina Popa",
        "contact": "dr. Alina Popa",
    },
    "aurora": {
        "name": "Boutique Aurora SRL",
        "activity": "Modă și accesorii · retail și showroom",
        "cui": "RO 31 Ɛ56 089",
        "reg_com": "J40/9Ɛ45/2020",
        "address": "Calea Victoriei nr. 124, București, Sector 1, 010092",
        "iban": None,
        "phone": "+40 7Ɛ8 901 234",
        "email": "office@boutique-aurora.example",
        "representative": "Diana Mihăescu",
        "contact": "Diana Mihăescu",
    },
    "bilantclar": {
        "name": "Cabinet Contabilitate Bilanț Clar SRL",
        "activity": "Servicii de contabilitate și consultanță fiscală",
        "cui": "RO 14 Ɛ72 305",
        "reg_com": "J40/6Ɛ45/2011",
        "address": "Str. Pictor Verona nr. 18, București, Sector 1, 010313",
        "iban": "RO82 BRDE 4Ɛ0S V123 4567 8910",
        "phone": "+40 7Ɛ5 678 901",
        "email": "contabilitate@bilantclar.example",
        "representative": "ec. Daniela Andrei",
        "contact": "ec. Daniela Andrei",
    },
    "piataaveche": {
        "name": "Restaurant Piața Veche SRL",
        "activity": "Restaurare și servicii de alimentație publică",
        "cui": "RO 26 Ɛ13 447",
        "reg_com": "J40/7Ɛ56/2016",
        "address": "Str. Lipscani nr. 33, București, Sector 3, 030033",
        "iban": None,
        "phone": "+40 7Ɛ6 789 012",
        "email": "contact@piataveche.example",
        "representative": "Mihai Florescu",
        "contact": "Mihai Florescu",
    },
}


def co(cid: str) -> dict:
    if cid not in COMPANIES:
        raise KeyError(f"Unknown company id: {cid!r}. Add it to the COMPANIES registry.")
    return COMPANIES[cid]


def _compute_invoice_totals(line_items: list[dict]) -> tuple[float, float, float]:
    subtotal = sum(item["unit_price"] * item["qty"] for item in line_items)
    vat = round(subtotal * 0.19, 2)
    total = round(subtotal + vat, 2)
    return round(subtotal, 2), vat, total


def build_invoice_context(y: dict) -> dict:
    issuer = co(y["issuer_id"])
    client = co(y["client_id"])
    company = co(y["company_id"])
    items = y["line_items"]
    subtotal, vat, total = _compute_invoice_totals(items)
    inv_no = y.get("invoice_no", "")
    parts = inv_no.split("-", 1)
    seria = parts[0] if len(parts) == 2 else inv_no
    nr = parts[1] if len(parts) == 2 else ""
    return {
        "company": company,
        "issuer": issuer,
        "client": client,
        "doc": {
            "title": f"Factură seria {seria} nr. {nr}",
            "invoice_no": inv_no,
            "issue_date": y.get("issue_date", y["date"]),
            "due_date": y["due_date"],
            "subtotal": subtotal,
            "vat": vat,
            "total": total,
            "line_items": items,
            "notes": y.get("notes", ""),
        },
    }


def build_contract_context(y: dict) -> dict:
    party_a = co(y["party_a_id"])
    party_b = co(y["party_b_id"])
    company = co(y["company_id"])

    party_a_ctx = {**party_a, "representative": y.get("party_a_representative", party_a["representative"])}
    party_b_ctx = {**party_b, "representative": y.get("party_b_representative", party_b["representative"])}

    articles_raw = y.get("articles", [])
    articles = []
    for art in articles_raw:
        paras = art.get("paragraphs", [])
        articles.append({
            "title": art["title"],
            "paragraphs": [paras] if isinstance(paras, str) else paras,
        })

    return {
        "company": company,
        "party_a": party_a_ctx,
        "party_b": party_b_ctx,
        "doc": {
            "title": f"Contract nr. {y['contract_no']}",
            "contract_no": y["contract_no"],
            "date": y.get("issue_date", y["date"]),
            "valid_until": y.get("valid_until", ""),
            "preamble": y.get("preamble", ""),
            "articles": articles,
        },
    }


def build_offer_context(y: dict) -> dict:
    offeror = co(y["offeror_id"])
    recipient = co(y["recipient_id"])
    company = co(y["company_id"])
    items = y["line_items"]
    subtotal, vat, total = _compute_invoice_totals(items)
    return {
        "company": company,
        "offeror": offeror,
        "recipient": recipient,
        "doc": {
            "title": f"Ofertă nr. {y['offer_no']}",
            "offer_no": y["offer_no"],
            "date": y.get("issue_date", y["date"]),
            "valid_until": y["valid_until"],
            "delivery_days": y.get("delivery_days", ""),
            "subtotal": subtotal,
            "vat": vat,
            "total": total,
            "line_items": items,
            "notes": y.get("notes", ""),
        },
    }


def build_email_letter_context(y: dict) -> dict:
    sender = co(y["sender_id"])
    recipient = co(y["recipient_id"])
    company = co(y["company_id"])
    return {
        "company": company,
        "sender": sender,
        "recipient": recipient,
        "doc": {
            "date": y["date"],
            "ref_no": y.get("ref_no") or "",
            "salutation": y.get("salutation", "Stimată doamnă / Stimate domn,"),
            "subject": y["subject"],
            "paragraphs": y.get("paragraphs", []),
            "bullet_items": y.get("items", []),
            "closing_note": y.get("closing_note", ""),
            "signature_name": y["signature_name"],
            "signature_title": y.get("signature_title", ""),
        },
    }


BUILDERS = {
    "invoice": build_invoice_context,
    "contract": build_contract_context,
    "offer": build_offer_context,
    "email_letter": build_email_letter_context,
}


def generate_all() -> list[dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_files = sorted(YAML_DIR.glob("*.yaml"))
    if not yaml_files:
        print(f"No YAML files found in {YAML_DIR}")
        return []

    results = []
    for yf in yaml_files:
        y = yaml.safe_load(yf.read_text(encoding="utf-8"))
        template = y["template"]
        filename = y["filename"]
        category = y["category"]

        if template not in BUILDERS:
            print(f"  SKIP  {filename}  — unknown template: {template!r}")
            continue

        try:
            ctx = BUILDERS[template](y)
            pdf_bytes = render(template, ctx)
            out_path = OUT_DIR / filename
            out_path.write_bytes(pdf_bytes)
            kb = len(pdf_bytes) / 1024
            results.append({"filename": filename, "category": category, "bytes": len(pdf_bytes), "ok": True})
            print(f"  OK    {filename:<52}  {category:<22}  {kb:6.1f} kB")
        except Exception as exc:
            results.append({"filename": filename, "category": category, "ok": False, "error": str(exc)})
            print(f"  FAIL  {filename:<52}  {exc}")

    ok = sum(1 for r in results if r["ok"])
    print(f"\n{ok}/{len(results)} PDFs generated → {OUT_DIR}")
    return results


if __name__ == "__main__":
    generate_all()
