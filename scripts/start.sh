#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

log()  { echo -e "${CYAN}[start]${NC} $*"; }
ok()   { echo -e "${GREEN}[ok]${NC}    $*"; }
warn() { echo -e "${YELLOW}[warn]${NC}  $*"; }
die()  { echo -e "${RED}[fail]${NC}  $*" >&2; exit 1; }

cleanup() {
  log "Shutting down …"
  kill "$API_PID" "$WEB_PID" 2>/dev/null || true
  wait "$API_PID" "$WEB_PID" 2>/dev/null || true
  ok "Done."
}

# ── 1. Postgres ───────────────────────────────────────────────────────────────
log "Starting Postgres (pgvector) …"
cd "$ROOT/infra"
docker compose up -d postgres

log "Waiting for Postgres to be healthy …"
for i in $(seq 1 20); do
  if docker compose exec -T postgres pg_isready -U bca -q 2>/dev/null; then
    ok "Postgres ready."; break
  fi
  [ "$i" -eq 20 ] && die "Postgres did not become ready in time."
  sleep 1
done

# ── 2. Migrations ─────────────────────────────────────────────────────────────
log "Running Alembic migrations …"
cd "$ROOT/apps/api"
uv run alembic upgrade head
ok "Migrations up to date."

# ── 3. API ────────────────────────────────────────────────────────────────────
log "Starting API on :8000 …"
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

# ── 4. Frontend ───────────────────────────────────────────────────────────────
log "Starting frontend on :5173 …"
cd "$ROOT/apps/web"
npm run dev &
WEB_PID=$!

# ── 5. Wait ───────────────────────────────────────────────────────────────────
trap cleanup INT TERM

echo ""
ok "Stack running:"
echo "  API      → http://localhost:8000"
echo "  Frontend → http://localhost:5173"
echo ""
echo "  Press Ctrl+C to stop all services."
echo ""

wait "$API_PID" "$WEB_PID"
