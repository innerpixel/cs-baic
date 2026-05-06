#!/usr/bin/env bash
# setup_slice5.sh — one-shot setup for slice-5 pgvector + fresh 8-doc seed
#
# Run from the repo root:
#   bash scripts/setup_slice5.sh
#
# Steps:
#   0. Check postgres has pgvector available (needs docker restart if not)
#   1. Run alembic upgrade head  (enables pgvector extension + creates document_chunks)
#   2. Wipe existing documents so reseed is clean
#   3. Seed all 8 demo docs via the running API

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API_DIR="$REPO_ROOT/apps/api"
INFRA_DIR="$REPO_ROOT/infra"
API_BASE="http://localhost:8000"

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
BLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "${GRN}✓${NC} $*"; }
warn() { echo -e "${YLW}!${NC} $*"; }
die()  { echo -e "${RED}✗ ERROR:${NC} $*"; exit 1; }
step() { echo -e "\n${BLD}$*${NC}"; }

echo ""
echo "=== slice-5 setup: pgvector + 8-doc seed ==="
echo ""

cd "$API_DIR"

# ── 0. Preflight: is pgvector available in the running postgres? ──────────────
step "0/4  Checking pgvector availability in postgres…"
PGVECTOR_AVAILABLE=$(uv run python - <<'PYEOF'
from app.db.session import SessionLocal
import sqlalchemy as sa
db = SessionLocal()
try:
    row = db.execute(sa.text("SELECT name FROM pg_available_extensions WHERE name='vector'")).fetchone()
    print("yes" if row else "no")
finally:
    db.close()
PYEOF
)

if [ "$PGVECTOR_AVAILABLE" != "yes" ]; then
    echo ""
    echo -e "${RED}✗ pgvector is not available in the running postgres container.${NC}"
    echo ""
    echo "The docker-compose.yml already has the right image (pgvector/pgvector:pg16)"
    echo "but the old container (postgres:16) is still running."
    echo ""
    echo -e "${BLD}You need to restart the container. Run these three commands in a terminal:${NC}"
    echo ""
    echo -e "  ${YLW}cd $INFRA_DIR${NC}"
    echo -e "  ${YLW}docker compose down${NC}"
    echo -e "  ${YLW}docker compose up -d postgres${NC}"
    echo ""
    echo "Wait ~10 seconds for postgres to start, then run this script again."
    echo ""
    echo "Note: your data will be preserved (volume is kept)."
    echo "If you hit issues after restart, add -v to 'docker compose down' to wipe the volume."
    exit 1
fi
ok "pgvector extension available in postgres"

# ── 1. Run alembic upgrade head ───────────────────────────────────────────────
step "1/4  Running alembic upgrade head…"
uv run alembic upgrade head

# Verify
uv run python - <<'PYEOF'
from app.db.session import SessionLocal
import sqlalchemy as sa
db = SessionLocal()
try:
    ext = db.execute(sa.text("SELECT extname, extversion FROM pg_extension WHERE extname='vector'")).fetchone()
    if not ext:
        raise RuntimeError("vector extension not present after migration")
    print(f"  vector extension v{ext.extversion} installed")
    chunks = db.execute(sa.text("SELECT COUNT(*) FROM document_chunks")).scalar()
    print(f"  document_chunks table: {chunks} rows")
    ver = db.execute(sa.text("SELECT version_num FROM alembic_version")).fetchall()
    print(f"  alembic head: {[v[0] for v in ver]}")
finally:
    db.close()
PYEOF
ok "Migration complete"

# ── 2. Wipe existing documents so reseed is clean ─────────────────────────────
step "2/4  Clearing existing documents…"
uv run python - <<'PYEOF'
from app.db.session import SessionLocal
import sqlalchemy as sa
db = SessionLocal()
try:
    count = db.execute(sa.text("SELECT COUNT(*) FROM documents")).scalar()
    if count > 0:
        db.execute(sa.text("DELETE FROM documents"))
        db.commit()
        print(f"  deleted {count} document(s) + cascaded chunks")
    else:
        print("  nothing to delete")
finally:
    db.close()
PYEOF
ok "Database cleared"

# ── 3. Check API is up, then seed ─────────────────────────────────────────────
step "3/4  Seeding 8 demo documents…"

if ! curl -sf "$API_BASE/api/documents" > /dev/null 2>&1; then
    echo ""
    echo -e "${RED}✗ API not responding at $API_BASE${NC}"
    echo ""
    echo -e "Start it first (in another terminal):"
    echo -e "  ${YLW}cd $API_DIR && uv run uvicorn app.main:app --reload${NC}"
    echo ""
    echo "Then re-run this script from step 3 manually:"
    echo "  cd $API_DIR && uv run python scripts/seed_demo.py"
    exit 1
fi

uv run python scripts/seed_demo.py

# ── 4. Final status ───────────────────────────────────────────────────────────
step "4/4  Status check…"
uv run python - <<'PYEOF'
from app.db.session import SessionLocal
import sqlalchemy as sa
db = SessionLocal()
try:
    docs     = db.execute(sa.text("SELECT COUNT(*) FROM documents")).scalar()
    done     = db.execute(sa.text("SELECT COUNT(*) FROM documents WHERE status='done'")).scalar()
    queued   = db.execute(sa.text("SELECT COUNT(*) FROM documents WHERE status='queued'")).scalar()
    chunks   = db.execute(sa.text("SELECT COUNT(*) FROM document_chunks")).scalar()
    with_emb = db.execute(sa.text("SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL")).scalar()
    print(f"  documents : {docs} total  ({done} done · {queued} still processing)")
    print(f"  chunks    : {chunks} total  ({with_emb} with embeddings)")
    if docs >= 8 and chunks > 0:
        print("\n  ✓ Ready. Test the live Ask endpoint:")
        print('    curl -s -X POST http://localhost:8000/api/ask \\')
        print('      -H "Content-Type: application/json" \\')
        print('      -d \'{"query":"Which invoices are urgent this week?"}\' | python3 -m json.tool')
    elif queued > 0:
        print(f"\n  ! {queued} doc(s) still processing — wait a moment then check again:")
        print("    curl http://localhost:8000/api/documents | python3 -m json.tool")
    else:
        print("\n  ! Some documents may have failed — check the seed output above")
finally:
    db.close()
PYEOF
