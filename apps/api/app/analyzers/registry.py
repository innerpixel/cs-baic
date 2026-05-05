from app.analyzers.invoice_extractor import InvoiceExtractor

ANALYZERS = [
    InvoiceExtractor(),
]


def analyzers_for(document) -> list:
    return [a for a in ANALYZERS if document.type in a.applies_to]
