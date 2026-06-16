#!/usr/bin/env bash
# Remote setup on Oracle VM after upload (run as ubuntu)
set -euo pipefail
APP_DIR=/opt/veridianwire
sudo mkdir -p "$APP_DIR/logs"
sudo useradd -r -m -d "$APP_DIR" -s /bin/bash newsbot 2>/dev/null || true
sudo chown -R newsbot:newsbot "$APP_DIR"
cd "$APP_DIR"
sudo -u newsbot python3 -m venv .venv
sudo -u newsbot bash -lc "source .venv/bin/activate && pip install -r requirements.txt"
if [ ! -f .env ]; then
  echo "Copy .env from your PC: scp .env ubuntu@IP:/tmp/ && sudo mv /tmp/.env $APP_DIR/.env && sudo chown newsbot:newsbot $APP_DIR/.env"
  exit 1
fi
sudo -u newsbot bash -lc "source .venv/bin/activate && python scripts/test_supabase.py"
sudo cp deploy/veridianwire-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now veridianwire-daemon
sudo systemctl status veridianwire-daemon --no-pager
echo "Pipeline running 24/7. Logs: tail -f $APP_DIR/logs/daemon.log"
