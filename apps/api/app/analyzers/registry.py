from app.analyzers.classifier import DocumentClassifier
from app.analyzers.summarizer import DocumentSummarizer
from app.analyzers.invoice_extractor import InvoiceExtractor
from app.analyzers.contract_reviewer import ContractReviewer

ANALYZERS = [
    DocumentClassifier(),
    DocumentSummarizer(),
    InvoiceExtractor(),
    ContractReviewer(),
]


def analyzers_for(document) -> list:
    return [a for a in ANALYZERS if document.type in a.applies_to]
