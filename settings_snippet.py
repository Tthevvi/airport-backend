# === Заменить соответствующие блоки в config/settings.py ===

import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = ["*"]  # на локальной разработке; в проде указать конкретные хосты

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # сторонние
    "rest_framework",
    "drf_spectacular",

    # наши приложения (по одному на сервис из компонентной диаграммы)
    "rest_framework.authtoken",
    "accounts",
    "references",
    "flights",
    "passengers",
    "bookings",
    "payments",
    "shifts",
    "refunds",
    "audit",
]

AUTH_USER_MODEL = "accounts.Cashier"   # своя модель пользователя вместо стандартной

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Airport Backend API",
    "DESCRIPTION": "АРМ кассира регионального аэропорта",
    "VERSION": "1.0.0",
}

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Asia/Novosibirsk"  # заменить на часовой пояс вашего аэропорта
USE_I18N = True
USE_TZ = True
