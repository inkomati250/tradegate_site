from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # note: settings/ is one level deeper

def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

def env_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

def env_list(key: str, default: str = "") -> list[str]:
    raw = os.getenv(key, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

SECRET_KEY = env("DJANGO_SECRET_KEY", "unsafe-dev-secret-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.sites",
    "django.contrib.sitemaps",

    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tradegate.urls"
WSGI_APPLICATION = "tradegate.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "website" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "website.context_processors.site_settings",
            ],
        },
    },
]

DB_NAME = env("DB_NAME", "")
if DB_NAME:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": env("DB_USER", ""),
            "PASSWORD": env("DB_PASSWORD", ""),
            "HOST": env("DB_HOST", "127.0.0.1"),
            "PORT": env("DB_PORT", "5432"),
            "CONN_MAX_AGE": int(env("DB_CONN_MAX_AGE", "60")),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", "en-us")
TIME_ZONE = env("DJANGO_TIME_ZONE", "Europe/Berlin")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATICFILES_DIRS = [BASE_DIR / "website" / "static"]
STATIC_ROOT = env("DJANGO_STATIC_ROOT", "/srv/tradegate/staticfiles")
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", "/srv/tradegate/media")

SITE_ID = int(env("DJANGO_SITE_ID", "1"))
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
EMAIL_TIMEOUT = int(env("EMAIL_TIMEOUT", "20"))

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "webmaster@localhost")
CONTACT_RECIPIENT_EMAIL = env("CONTACT_RECIPIENT_EMAIL", "")
