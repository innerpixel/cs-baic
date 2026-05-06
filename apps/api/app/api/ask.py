from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ask import AskAnswer
from app.services.ask import answer_question

router = APIRouter()


class AskRequest(BaseModel):
    query: str


@router.post("/ask", response_model=AskAnswer)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    return answer_question(request.query, db)
