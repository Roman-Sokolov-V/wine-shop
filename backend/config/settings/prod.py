from .dev import *

DEBUG = False

MINIO_STORAGE_MEDIA_URL = (
    "https://sha-man.pp.ua/minio/shelter-bucket"  # Для генерації URL
)
CELERY_BROKER_URL = "redis://redis:6379/0"


ALLOWED_HOSTS = ["sha-man.pp.ua", "3.120.102.6", "shelter"]
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
    "http://localhost",
    "http://localhost:3000",
    "https://91.193.174.2",
    "https://syavayki.github.io",
    "http://syavayki.github.io",
]

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://91.193.174.2",
    "https://syavayki.github.io",
    "http://syavayki.github.io",
]
