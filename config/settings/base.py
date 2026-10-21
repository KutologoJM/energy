"""
Base settings for energy_monitor.

This file is the base for the settings package.

Settings package layout:
    settings/
    ├── __init__.py
    ├── base.py       ← you are here
    ├── dev.py        ← overrides for local development
    └── production.py ← overrides for production deployment

Usage:
    DJANGO_SETTINGS_MODULE=config.settings.dev
    DJANGO_SETTINGS_MODULE=config.settings.production

Docs: https://docs.djangoproject.com/en/stable/topics/settings/
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import importlib


# ==============================================================================
# PATHS
# ==============================================================================
"""
BASE_DIR resolves to the project root (three .parent calls because this file
lives at config/settings/base.py inside the settings package).
"""
BASE_DIR = Path(__file__).resolve().parents[2]
# checks if BASE_DIR generated in the expected directory
if not (BASE_DIR / "manage.py").is_file():
    raise ImproperlyConfigured(
        f"BASE_DIR is wrong: {BASE_DIR} has no manage.py. "
        "Expected settings at energy_monitor/config/settings/base.py."
    )
# ==============================================================================
# CORE
# ==============================================================================
from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version("energy_monitor")
except PackageNotFoundError:
    VERSION = "0.0.0-dev"

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True

# ==============================================================================
# ENVIRONMENT
# ==============================================================================

import environ

env = environ.Env(
    DEBUG=(bool, False), )
environ.Env.read_env(BASE_DIR / ".env")
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# ==============================================================================
# ADMINS
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#admins
# ==============================================================================

from email.utils import getaddresses

ADMINS = getaddresses([env("ADMINS", default="")])
MANAGERS = ADMINS

# ==============================================================================
# APPLICATIONS
# ==============================================================================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # third party but needs to be before django.contrib.staticfiles
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "django_filters",
     "health_check", 
    
    
    
]

CONFIG_APPS = [
    "apps.accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
]

LOCAL_APPS = [

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CONFIG_APPS + LOCAL_APPS

if "apps.accounts.apps.AccountsConfig" not in INSTALLED_APPS:
    raise ImproperlyConfigured(
        "AUTH_USER_MODEL requires 'apps.accounts.apps.AccountsConfig' to be in INSTALLED_APPS."
    )

try:
    importlib.import_module("apps.accounts")
except ModuleNotFoundError as e:
    raise ImproperlyConfigured(
        f"'apps.accounts' is listed in INSTALLED_APPS but could not be imported: {e}"
    ) from e

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

AUTH_USER_MODEL = "accounts.User"

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================================================================
# TEMPLATES
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#templates
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # noqa
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# PASSWORD VALIDATION
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# INTERNATIONALISATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC FILES
# ==============================================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # collecstatic output directory
STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",  # suggest switching to S3 in prod
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==============================================================================
# SECURITY
# Docs: https://docs.djangoproject.com/en/stable/topics/security/
# ==============================================================================

# Redirect all HTTP requests to HTTPS.
SECURE_SSL_REDIRECT = True
# Prevent browsers from guessing content types (MIME sniffing).
SECURE_CONTENT_TYPE_NOSNIFF = True
# Tell browsers to only send cookies over HTTPS.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Prevent this site from being embedded in an iframe on another origin.
X_FRAME_OPTIONS = "DENY"
# This tells Django to trust the X-Forwarded-Proto header set by the proxy instead of checking the raw connection.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ==============================================================================
# LOGGING
# Docs: https://docs.djangoproject.com/en/stable/topics/logging/
# ==============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },

}

# ==============================================================================
# HEALTH CHECK
# Docs: https://django-health-check.readthedocs.io/en/stable/
# ==============================================================================

HEALTH_CHECK_TOKEN = env("HEALTH_CHECK_TOKEN")









