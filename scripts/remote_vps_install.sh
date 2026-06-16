#!/usr/bin/env bash
# Full remote install after deploy_to_vps.ps1 uploads files (run on Oracle VM as ubuntu)
set -euo pipefail
APP_DIR=/opt/veridianwire

sudo apt-get update -qq
sudo apt-get install -y python3 python3-venv python3-pip unzip

sudo mkdir -p "$APP_DIR"
sudo unzip -o /tmp/veridianwire-pipeline.zip -d "$APP_DIR"
sudo mv /tmp/veridianwire.env "$APP_DIR/.env"
sudo mkdir -p "$APP_DIR/logs"
sudo useradd -r -m -d "$APP_DIR" -s /bin/bash newsbot 2>/dev/null || true
sudo chown -R newsbot:newsbot "$APP_DIR"
sudo chmod 600 "$APP_DIR/.env"

cd "$APP_DIR"
sudo -u newsbot python3 -m venv .venv
sudo -u newsbot bash -lc 'source .venv/bin/activate && pip install -q -r requirements-daemon.txt'
sudo -u newsbot bash -lc 'source .venv/bin/activate && python scripts/test_supabase.py'

sudo cp deploy/veridianwire-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now veridianwire-daemon
sleep 2
sudo systemctl status veridianwire-daemon --no-pager || true
echo "=== tail daemon log ==="
sudo tail -n 20 "$APP_DIR/logs/daemon.log" 2>/dev/null || echo "(log not yet created)"
