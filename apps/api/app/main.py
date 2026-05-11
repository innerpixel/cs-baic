import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NovAI Desk API", version="0.7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


from app.api.documents import router as documents_router
from app.api.audit import router as audit_router
from app.api.ask import router as ask_router
from app.api.uploads import router as uploads_router
from app.api.demo import router as demo_router

app.include_router(documents_router, prefix="/api")
app.include_router(audit_router, prefix="/api")
app.include_router(ask_router, prefix="/api")
app.include_router(uploads_router, prefix="/api")
app.include_router(demo_router, prefix="/api")

# Internal text upload — only mounted when explicitly enabled (dev + eval environments)
if os.getenv("ENABLE_INTERNAL_TEXT_UPLOAD", "true").lower() == "true":
    from app.api._internal.uploads import router as internal_uploads_router
    app.include_router(internal_uploads_router, prefix="/api")
