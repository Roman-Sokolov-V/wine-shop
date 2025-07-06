from .dev import *

DEBUG = True

ALLOWED_HOSTS = ["sha-man.pp.ua", "3.120.102.6"]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_HTTPONLY = True

CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "https://91.193.174.2",
    "https://syavayki.github.io"
]

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "https://localhost:3000",
    "https://91.193.174.2",
    "https://syavayki.github.io"
]
