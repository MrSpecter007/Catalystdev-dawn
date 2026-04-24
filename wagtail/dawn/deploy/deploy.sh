#!/usr/bin/env bash
# Hostinger VPS deployment script for Dawn (Wagtail)
# Run on the VPS as root: bash deploy.sh
set -euo pipefail

REPO_URL="https://github.com/MrSpecter007/Catalystdev-dawn.git"
BRANCH="main"
REPO_DIR="/var/www/catalystdev-dawn"
APP_DIR="$REPO_DIR/wagtail/dawn"
PYTHON="python3.12"

echo "==> Installing system packages"
apt-get update -q
apt-get install -y -q \
    git nginx python3.12 python3.12-venv python3.12-dev \
    default-libmysqlclient-dev build-essential pkg-config \
    mysql-server certbot python3-certbot-nginx

echo "==> Cloning / pulling repo"
if [ -d "$REPO_DIR/.git" ]; then
    git -C "$REPO_DIR" fetch origin "$BRANCH"
    git -C "$REPO_DIR" reset --hard "origin/$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
fi

echo "==> Setting up Python virtual environment"
if [ ! -d "$APP_DIR/venv" ]; then
    "$PYTHON" -m venv "$APP_DIR/venv"
fi
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "==> Setting up .env"
if [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo ""
    echo "  !! .env created. Edit it now before continuing:"
    echo "     nano $APP_DIR/.env"
    echo "  Then re-run this script."
    exit 1
fi

# Load env vars for management commands
set -a; source "$APP_DIR/.env"; set +a

echo "==> Running migrations"
cd "$APP_DIR"
"$APP_DIR/venv/bin/python" manage.py migrate --noinput

echo "==> Collecting static files"
"$APP_DIR/venv/bin/python" manage.py collectstatic --noinput --clear

echo "==> Fixing permissions"
chown -R www-data:www-data "$REPO_DIR"
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
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo ""
echo "==> Deployment complete!"
echo "    Site: http://187.127.252.86"
echo "    Admin: http://187.127.252.86/admin"
echo ""
echo "    When you have a domain:"
echo "    1. Update nginx.conf server_name and run: certbot --nginx -d yourdomain.com"
echo "    2. Set HTTPS=true in $APP_DIR/.env and restart: systemctl restart dawn"
