"""
App configuration for Django's application registry.

Docs: https://docs.djangoproject.com/en/stable/ref/applications/

Rules:
    - Set default_auto_field to avoid implicit primary key warnings.
    - Use ready() to connect signals if necessary.

"""

from django.apps import AppConfig

class MonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.monitor'
