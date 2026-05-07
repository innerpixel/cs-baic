#!/usr/bin/env bash
# setup.sh — check dependencies, install what's missing, boot the stack
#
# Usage:
#   ./setup.sh          — check + install + start postgres + run migrations
#   ./setup.sh --seed   — also run seed_invoices.py after migrations
#   ./setup.sh --help   — this message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$SCRIPT_DIR/apps/api"
WEB_DIR="$SCRIPT_DIR/apps/web"
INFRA_DIR="$SCRIPT_DIR/infra"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
err()  { echo -e "${RED}✗${NC} $*"; }
step() { echo -e "\n${YELLOW}──${NC} $*"; }

SEED=false
for arg in "$@"; do
  case "$arg" in
    --seed) SEED=true ;;
    --help)
      echo "Usage: ./setup.sh [--seed] [--help]"
      echo "  --seed   Run seed_invoices.py after migrations"
      echo "  --help   Show this message"
      exit 0
      ;;
  esac
done

# ── 1. Node.js / npm ──────────────────────────────────────────────────────────

step "Checking Node.js"
if command -v node &>/dev/null && command -v npm &>/dev/null; then
  ok "node $(node --version)  npm $(npm --version)"
else
  err "Node.js not found."
  echo "   Install from https://nodejs.org or via nvm:"
  echo "   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"
  echo "   nvm install --lts"
  exit 1
fi

# ── 2. uv (Python package manager) ───────────────────────────────────────────

step "Checking uv"
if command -v uv &>/dev/null; then
  ok "uv $(uv --version)"
else
  warn "uv not found — installing via official installer"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # reload PATH for this session
  export PATH="$HOME/.local/bin:$PATH"
  if command -v uv &>/dev/null; then
    ok "uv installed: $(uv --version)"
  else
    err "uv installation failed. Install manually: https://docs.astral.sh/uv/"
    exit 1
  fi
fi

# ── 3. Docker ─────────────────────────────────────────────────────────────────

step "Checking Docker"
if command -v docker &>/dev/null; then
  ok "docker $(docker --version)"
else
  warn "Docker not found — installing Docker Engine for Ubuntu"

  if ! command -v apt-get &>/dev/null; then
    err "apt-get not available. Install Docker manually: https://docs.docker.com/engine/install/"
    exit 1
  fi

  echo "   Running: sudo apt-get update && sudo apt-get install -y ca-certificates curl"
  sudo apt-get update -qq
  sudo apt-get install -y -qq ca-certificates curl

  echo "   Adding Docker GPG key and repository"
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update -qq
  sudo apt-get install -y -qq \
    docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin

  ok "Docker installed: $(docker --version)"
fi

# Ensure current user can talk to the Docker socket without sudo
if ! docker info &>/dev/null 2>&1; then
  if ! groups "$USER" | grep -q docker; then
    warn "Adding $USER to the docker group"
    sudo usermod -aG docker "$USER"
  fi
  # Re-exec entire script under sg so the new group takes effect immediately
  warn "Re-launching script with docker group active (sg docker)..."
  exec sg docker -c "bash \"$0\" $*"
fi

# Verify docker compose (v2 plugin)
if ! docker compose version &>/dev/null; then
  err "docker compose plugin not found. Ensure docker-compose-plugin is installed."
  exit 1
fi
ok "docker compose $(docker compose version --short)"

# ── 4. Python dependencies for apps/api ──────────────────────────────────────

step "Installing Python dependencies (apps/api)"
cd "$API_DIR"
uv sync --quiet
ok "Python venv ready"

# ── 5. Node dependencies for apps/web ────────────────────────────────────────

step "Installing Node dependencies (apps/web)"
cd "$WEB_DIR"
npm install --silent
ok "Node modules ready"

# ── 6. .env files ────────────────────────────────────────────────────────────

step "Checking .env files"

if [ ! -f "$INFRA_DIR/.env" ]; then
  cp "$INFRA_DIR/.env.example" "$INFRA_DIR/.env"
  warn "Created infra/.env from .env.example — edit LLM_API_KEY before seeding"
else
  ok "infra/.env exists"
fi

if [ ! -f "$API_DIR/.env" ]; then
  cp "$INFRA_DIR/.env.example" "$API_DIR/.env"
  warn "Created apps/api/.env from .env.example — edit LLM_API_KEY before seeding"
else
  ok "apps/api/.env exists"
fi

# ── 7. Start Postgres ─────────────────────────────────────────────────────────

step "Starting Postgres"
cd "$INFRA_DIR"
docker compose up -d postgres

echo "   Waiting for Postgres to be ready..."
for i in $(seq 1 20); do
  if docker compose exec -T postgres pg_isready -q 2>/dev/null; then
    ok "Postgres is ready"
    break
  fi
  if [ "$i" -eq 20 ]; then
    err "Postgres did not become ready in time. Check: docker compose logs postgres"
    exit 1
  fi
  sleep 1
done

# ── 8. Run Alembic migrations ─────────────────────────────────────────────────

step "Running database migrations"
cd "$API_DIR"
uv run alembic upgrade head
ok "Migrations applied"

# ── 9. Seed (optional) ────────────────────────────────────────────────────────

if [ "$SEED" = true ]; then
  step "Seeding demo invoices"
  echo "   Starting API temporarily for seeding..."

  # Start API in background
  uv run uvicorn app.main:app --port 8000 &
  API_PID=$!

  # Wait for API to start
  for i in $(seq 1 15); do
    if curl -s http://localhost:8000/api/health &>/dev/null; then
      ok "API ready on :8000"
      break
    fi
    if [ "$i" -eq 15 ]; then
      kill "$API_PID" 2>/dev/null || true
      err "API did not start in time"
      exit 1
    fi
    sleep 1
  done

  uv run python scripts/seed_invoices.py
  kill "$API_PID" 2>/dev/null || true
  wait "$API_PID" 2>/dev/null || true
  ok "Seeding complete"
fi

# ── Done ─────────────────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}┌─────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│  Stack is ready                             │${NC}"
echo -e "${GREEN}└─────────────────────────────────────────────┘${NC}"
echo ""
echo "  Start the API:       cd apps/api && uv run uvicorn app.main:app --reload"
echo "  Start the frontend:  cd apps/web && npm run dev"
echo ""
if [ "$SEED" = false ]; then
  echo "  Seed demo invoices (with API running):"
  echo "    cd apps/api && uv run python scripts/seed_invoices.py"
  echo ""
fi
echo "  API health:          http://localhost:8000/api/health"
echo "  Frontend:            http://localhost:5173"
echo ""
