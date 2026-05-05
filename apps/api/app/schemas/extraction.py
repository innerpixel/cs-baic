from pydantic import BaseModel


class LineItem(BaseModel):
    description: str | None = None
    quantity: str | None = None
    unit_price: str | None = None
    amount: str | None = None


class InvoiceExtraction(BaseModel):
    supplier_name: str | None = None
    supplier_cui: str | None = None
    supplier_vat_number: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    total_amount: str | None = None
    vat_amount: str | None = None
    currency: str | None = None
    iban: str | None = None
    payment_status: str = "unknown"
    line_items: list[LineItem] = []
    missing_fields: list[str] = []
    risk_flags: list[str] = []
    recommended_next_action: str | None = None
