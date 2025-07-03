from dev import *

DEBUG = True

ALLOWED_HOSTS = ["*"]  # TODO змінити
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.1.105",
    "http://91.193.174.2",
]

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://3.120.102.6",
]
# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'None'
# CSRF_COOKIE_HTTPONLY = False
