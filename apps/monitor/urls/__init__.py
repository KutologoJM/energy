"""
URL routing for DRF API endpoints.

Docs: https://www.django-rest-framework.org/api-guide/routers/

Rules:
    - Mount these under /api/v1/ in the root urls.py using include().
    - Use an app_name for namespacing so reverse() calls are unambiguous.

Example:
    # root urls.py
    path("api/v1/", include(("posts.urls.api", "posts_api"), namespace="posts_api")),

    # this file
    urlpatterns = [
        path("posts/", PostListCreateView.as_view(), name="post-list-create"),
        path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    ]
"""
from django.urls import path
from apps.monitor import views
urlpatterns = [
path("", views.index, name="index"),
    path("new-reading", views.process_new_reading)
]
