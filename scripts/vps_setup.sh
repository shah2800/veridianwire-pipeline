#!/usr/bin/env bash
# One-time VPS setup for 24/7 news pipeline (Ubuntu 22.04+)
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/veridianwire}"
APP_USER="${APP_USER:-newsbot}"

echo "==> Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y python3 python3-venv python3-pip git curl

echo "==> Creating user $APP_USER..."
id "$APP_USER" &>/dev/null || sudo useradd -r -m -d "$APP_DIR" -s /bin/bash "$APP_USER"

echo "==> App directory: $APP_DIR"
sudo mkdir -p "$APP_DIR/logs"
sudo chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo ""
echo "Next steps (run as $APP_USER or copy project into $APP_DIR):"
echo "  1. Clone/copy project to $APP_DIR"
echo "  2. cp .env.example .env && nano .env   # add API keys"
echo "  3. python3 -m venv .venv && source .venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. python scripts/test_supabase.py"
echo "  6. sudo cp deploy/veridianwire-daemon.service /etc/systemd/system/"
echo "  7. sudo systemctl daemon-reload"
echo "  8. sudo systemctl enable --now veridianwire-daemon"
echo "  9. sudo systemctl status veridianwire-daemon"
