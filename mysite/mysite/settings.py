"""
Paramètres Django pour le projet « mysite ».

– Pensé pour être hybride : SQLite en développement, PostgreSQL en production
– Utilise SimpleJWT + Firebase Auth pour l’API
– Charge la configuration via des variables d’environnement (.env)
"""

import os
from pathlib import Path
from datetime import timedelta
from django.core.management.utils import get_random_secret_key

# ─────────────────────────────────────────────────────────────
# 1. Chemins & environnement
# ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ENV = os.getenv("DJANGO_ENV", "dev")          # dev | prod
DEBUG = os.getenv("DEBUG", "True") == "True"

# ─────────────────────────────────────────────────────────────
# 2. Templates
# ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ─────────────────────────────────────────────────────────────
# 3. Sécurité
# ─────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY") or get_random_secret_key()
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ─────────────────────────────────────────────────────────────
# 4. Applications
# ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tiers
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "drf_spectacular",

    # Projet
    "core",
    "users",
]

# ─────────────────────────────────────────────────────────────
# 5. Middleware
# ─────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"
ASGI_APPLICATION = "mysite.asgi.application"

# ─────────────────────────────────────────────────────────────
# 6. Bases de données
# ─────────────────────────────────────────────────────────────
if ENV == "prod":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "mysite"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─────────────────────────────────────────────────────────────
# 7. Authentification et API REST
# ─────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "core.authentication.FirebaseAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# SimpleJWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_MINUTES", 30))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_DAYS", 7))),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ─────────────────────────────────────────────────────────────
# 8. drf-spectacular (documentation API)
# ─────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "Mutooni API",
    "DESCRIPTION": "Documentation de l'API Mutooni avec Swagger et ReDoc",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ─────────────────────────────────────────────────────────────
# 9. Internationalisation
# ─────────────────────────────────────────────────────────────
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = os.getenv("TZ", "Africa/Dakar")
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────────
# 10. Fichiers statiques / médias
# ─────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─────────────────────────────────────────────────────────────
# 11. CORS (accès depuis Flutter web, etc.)
# ─────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# ─────────────────────────────────────────────────────────────
# 12. Firebase (facultatif)
# ─────────────────────────────────────────────────────────────
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")  # Chemin vers serviceAccountKey.json
