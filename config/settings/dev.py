"""
Development settings for energy_monitor.

Usage:
    DJANGO_SETTINGS_MODULE=config.settings.dev

Docs: https://docs.djangoproject.com/en/stable/topics/settings/
"""
from .base import *  # noqa: F403

# ==============================================================================
# CORE
# ==============================================================================

DEBUG = env("DEBUG")

INTERNAL_IPS = [
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")  # noqa: F405

# ==============================================================================
# DATABASE
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#databases
# ==============================================================================


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# SECURITY OVERRIDES
# Docs: https://docs.djangoproject.com/en/stable/topics/security/
# ==============================================================================
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ==============================================================================
# APPLICATIONS
# ==============================================================================

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
    "django_watchfiles"
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("whitenoise.middleware.WhiteNoiseMiddleware") + 1,  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,  # noqa: F405
    "django_browser_reload.middleware.BrowserReloadMiddleware",
)

# ==============================================================================
# EMAIL
# Docs: https://docs.djangoproject.com/en/stable/topics/email/#console-backend
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ==============================================================================
# CACHING
# ==============================================================================


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
