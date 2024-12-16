from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "labdev",  # Nombre DB
        "USER": "root",  # Nombre usuario
        "PASSWORD": "cpce1901",  # Password
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static/"]

DOCUMENTS_URL = 'documents/'
DOCUMENTS_ROOT = BASE_DIR / "documents/"