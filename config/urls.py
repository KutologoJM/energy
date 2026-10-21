"""
URL configuration for energy_monitor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from health_check.views import HealthCheckView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path(
        f"health/{settings.HEALTH_CHECK_TOKEN}/",
        HealthCheckView.as_view(
            checks=[
                "health_check.DNS",
                "health_check.Cache",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                # 3rd party checks
                "health_check.contrib.psutil.CPU",
                "health_check.contrib.psutil.Memory",
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Temperature",
                # "health_check.contrib.atlassian.Cloudflare",
                # "health_check.contrib.atlassian.Render",
            ]
        ),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(
            "__debug__", include(debug_toolbar.urls)
        ),  # This registers the 'djdt' namespace
        path("__reload__/", include("django_browser_reload.urls")),
    ]
