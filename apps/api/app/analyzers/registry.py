from app.analyzers.classifier import DocumentClassifier
from app.analyzers.summarizer import DocumentSummarizer
from app.analyzers.invoice_extractor import InvoiceExtractor
from app.analyzers.contract_reviewer import ContractReviewer
from app.analyzers.draft_reply_generator import DraftReplyGenerator
from app.analyzers.document_indexer import DocumentIndexer

ANALYZERS = [
    DocumentClassifier(),
    DocumentSummarizer(),
    InvoiceExtractor(),
    ContractReviewer(),
    DraftReplyGenerator(),
    DocumentIndexer(),
]


def analyzers_for(document) -> list:
    return [a for a in ANALYZERS if document.type in a.applies_to]
