import os

from .base import *

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

_scheme = "https" if os.environ.get("HTTPS", "false").lower() == "true" else "http"
CSRF_TRUSTED_ORIGINS = [
    f"{_scheme}://{host}" for host in ALLOWED_HOSTS if host
]

# Database — MySQL on Hostinger VPS
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Security headers — set HTTPS=true in .env once SSL is configured
_https = os.environ.get("HTTPS", "false").lower() == "true"
SECURE_SSL_REDIRECT = _https
SESSION_COOKIE_SECURE = _https
CSRF_COOKIE_SECURE = _https
SECURE_HSTS_SECONDS = 31536000 if _https else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = _https
SECURE_HSTS_PRELOAD = _https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if _https else None

# Wagtail
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "https://example.com")

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")

try:
    from .local import *
except ImportError:
    pass
