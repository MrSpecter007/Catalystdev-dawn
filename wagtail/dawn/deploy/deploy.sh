#!/usr/bin/env bash
# Hostinger VPS deployment script for Dawn (Wagtail)
# Run this on the VPS as root (or sudo), then subsequent runs as www-data via sudo.
# Usage: bash deploy/deploy.sh

set -euo pipefail

APP_DIR="/var/www/dawn"
REPO_URL="https://github.com/YOUR_ORG/YOUR_REPO.git"   # <-- replace
BRANCH="main"
PYTHON="python3.12"

echo "==> Installing system packages"
apt-get update -q
apt-get install -y -q \
    git nginx python3.12 python3.12-venv python3.12-dev \
    default-libmysqlclient-dev build-essential \
    certbot python3-certbot-nginx

echo "==> Creating app directory"
mkdir -p "$APP_DIR"
chown www-data:www-data "$APP_DIR"

echo "==> Cloning / pulling repo"
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" fetch origin "$BRANCH"
    git -C "$APP_DIR" reset --hard "origin/$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

echo "==> Setting up Python virtual environment"
if [ ! -d "$APP_DIR/venv" ]; then
    "$PYTHON" -m venv "$APP_DIR/venv"
fi
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "==> Setting up .env (skip if already exists)"
if [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo "  !! Edit $APP_DIR/.env before continuing !!"
    exit 1
fi

# Load env vars for management commands
set -a; source "$APP_DIR/.env"; set +a

echo "==> Running migrations"
"$APP_DIR/venv/bin/python" "$APP_DIR/manage.py" migrate --noinput

echo "==> Collecting static files"
"$APP_DIR/venv/bin/python" "$APP_DIR/manage.py" collectstatic --noinput --clear

echo "==> Fixing permissions"
chown -R www-data:www-data "$APP_DIR"
mkdir -p /var/log/dawn
chown -R www-data:www-data /var/log/dawn

echo "==> Installing systemd service"
cp "$APP_DIR/deploy/dawn.service" /etc/systemd/system/dawn.service
systemctl daemon-reload
systemctl enable dawn
systemctl restart dawn

echo "==> Installing nginx config"
cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/dawn
ln -sf /etc/nginx/sites-available/dawn /etc/nginx/sites-enabled/dawn
nginx -t
systemctl reload nginx

echo ""
echo "==> Done! Next steps:"
echo "  1. Edit $APP_DIR/.env with your real values"
echo "  2. Run: certbot --nginx -d yourdomain.com -d www.yourdomain.com"
echo "  3. Visit https://yourdomain.com/admin to verify"
