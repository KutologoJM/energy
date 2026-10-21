"""
Production settings for energy_monitor.

Inherits all production-safe defaults from base.py. Only add settings here
that require real production credentials.

Usage:
    DJANGO_SETTINGS_MODULE=config.settings.production

Docs: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
"""

from .base import *  # noqa: F403

# ==============================================================================
# SECURITY
# ==============================================================================


# ==============================================================================
# DATABASE
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#databases
# ==============================================================================


DATABASES = {"default": env.db()}


# ==============================================================================
# CACHE
# Docs: https://docs.djangoproject.com/en/stable/topics/cache/
# ==============================================================================


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        # Run: python manage.py createcachetable
    }
}


# ==============================================================================
# EMAIL
# Docs: https://docs.djangoproject.com/en/stable/topics/email/#smtp-backend
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
