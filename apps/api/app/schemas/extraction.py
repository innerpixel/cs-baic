from pydantic import BaseModel, field_validator


def _coerce_monetary(v: object) -> str | None:
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, (int, float)):
        return f"{float(v):.2f}"
    return str(v)


def _coerce_integer(v: object) -> str | None:
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, (int, float)):
        return str(int(v))
    return str(v)


class LineItem(BaseModel):
    description: str | None = None
    quantity: str | None = None
    unit_price: str | None = None
    amount: str | None = None

    @field_validator("unit_price", "amount", mode="before")
    @classmethod
    def coerce_monetary(cls, v: object) -> str | None:
        return _coerce_monetary(v)

    @field_validator("quantity", mode="before")
    @classmethod
    def coerce_quantity(cls, v: object) -> str | None:
        return _coerce_integer(v)


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

    @field_validator("total_amount", "vat_amount", mode="before")
    @classmethod
    def coerce_monetary(cls, v: object) -> str | None:
        return _coerce_monetary(v)
