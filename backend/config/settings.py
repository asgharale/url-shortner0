import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "mini2.ir", "www.mini2.ir",
    "tny2.ir", "www.tny2.ir",
    "sml2.ir", "www.sml2.ir",
    "shrtlnk.ir", "www.shrtlnk.ir",
    "linksml.ir", "www.linksml.ir",
    "charkhoon2.ir", "www.charkhoon2.ir",
    "kootaher.ir", "www.kootaher.ir",
    "localhost", "127.0.0.1",
]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "shortener",
]

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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "https://mini2.ir")

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "https://mini2.ir,https://www.mini2.ir,"
    "https://tny2.ir,https://www.tny2.ir,"
    "https://sml2.ir,https://www.sml2.ir,"
    "https://shrtlnk.ir,https://www.shrtlnk.ir,"
    "https://linksml.ir,https://www.linksml.ir,"
    "https://kootaher.ir,https://www.kootaher.ir,"
    "https://charkhoon2.ir,https://www.charkhoon2.ir",
).split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://mini2.ir,https://www.mini2.ir,"
    "https://tny2.ir,https://www.tny2.ir,"
    "https://sml2.ir,https://www.sml2.ir,"
    "https://shrtlnk.ir,https://www.shrtlnk.ir,"
    "https://linksml.ir,https://www.linksml.ir,"
    "https://kootaher.ir,https://www.kootaher.ir,"
    "https://charkhoon2.ir,https://www.charkhoon2.ir",
).split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Used by the ORIGINAL shortener's frontend domain-tab picker
ALLOWED_SHORT_DOMAINS = os.environ.get(
    "ALLOWED_SHORT_DOMAINS", "mini2.ir,tny2.ir"
).split(",")

# Used by the PRO shortener — every short link is shown across all 4 of these at once
ALLOWED_PRO_DOMAINS = os.environ.get(
    "ALLOWED_PRO_DOMAINS", "sml2.ir,shrtlnk.ir,linksml.ir,kootaher.ir"
).split(",")