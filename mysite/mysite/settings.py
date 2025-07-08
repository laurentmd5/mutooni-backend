import os
from pathlib import Path
from datetime import timedelta
from django.core.management.utils import get_random_secret_key
from corsheaders.defaults import default_headers

# ─────────────────────────────────────────────
# 1. Chemins & Environnement
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ENV = os.getenv("DJANGO_ENV", "dev")  # dev | prod
DEBUG = os.getenv("DEBUG", "True") == "True"

# ─────────────────────────────────────────────
# 2. Logging
# ─────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
        'django.security': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
        'rest_framework': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
    },
}

# ─────────────────────────────────────────────
# 3. Templates
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 4. Sécurité
# ─────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY") or get_random_secret_key()
ALLOWED_HOSTS = ["*", "192.168.61.131"]

# ─────────────────────────────────────────────
# 5. Applications
# ─────────────────────────────────────────────
INSTALLED_APPS = [
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

# ─────────────────────────────────────────────
# 6. Middleware
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 7. Base de données
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 8. Authentification & API REST
# ─────────────────────────────────────────────
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # ✅ requis pour OpenAPI
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_MINUTES", 30))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_DAYS", 7))),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ─────────────────────────────────────────────
# 9. drf-spectacular (OpenAPI/Swagger)
# ─────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "Mutooni API",
    "DESCRIPTION": "Documentation de l'API Mutooni avec Swagger et ReDoc",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
}

# ─────────────────────────────────────────────
# 10. Internationalisation
# ─────────────────────────────────────────────
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = os.getenv("TZ", "Africa/Dakar")
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# 11. Statics & Médias
# ─────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─────────────────────────────────────────────
# 12. CORS (Flutter Web & autres clients)
# ─────────────────────────────────────────────
CORS_ALLOW_CREDENTIALS = True

# Ajoutez cette ligne pour autoriser toutes les origines en développement
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Mettez à jour cette liste avec toutes vos origines
CORS_ALLOWED_ORIGINS = [
    "https://9002-firebase-mutooni-front-1751399486531.cluster-l6vkdperq5ebaqo3qy4ksvoqom.cloudworkstations.dev",
    "https://9000-firebase-mutooni-front-1751399486531.cluster-l6vkdperq5ebaqo3qy4ksvoqom.cloudworkstations.dev",
    "http://localhost:8000",
    "http://10.88.0.3:9000",
    "http://10.88.0.3:9002",
    "http://localhost:5271",
    "https://8000-firebase-mutooni-back-1751236955562.cluster-l6vkdperq5ebaqo3qy4ksvoqom.cloudworkstations.dev",
    "http://192.168.61.131:8000",
]

# Ajoutez cette regex pour autoriser tous les sous-domaines
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/(\d+)-firebase-mutooni-(front|back)-.+\.cloudworkstations\.dev$"
]

# Ajoutez ces headers supplémentaires
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
    "content-type",
    "x-requested-with",
]

# Ajoutez ces méthodes
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]

# ─────────────────────────────────────────────
# 13. Firebase
# ─────────────────────────────────────────────
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

if FIREBASE_CREDENTIALS:
    try:
        # Décoder les credentials si nécessaire
        import json
        FIREBASE_CONFIG = json.loads(FIREBASE_CREDENTIALS)
    except json.JSONDecodeError:
        FIREBASE_CONFIG = None
else:
    FIREBASE_CONFIG = None