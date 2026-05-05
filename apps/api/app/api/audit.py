from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.models import AuditEvent
from app.db.session import get_db
from app.schemas.documents import AuditEventOut

router = APIRouter()


@router.get("/audit", response_model=list[AuditEventOut])
def list_audit_events(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    return db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit).all()
