"""
DRF filter classes for URL query parameter filtering on list endpoints.

Docs: https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html

Rules:
    - Use FilterSet subclasses from django_filters.rest_framework.
    - Filters handle URL param filtering only: e.g. /api/posts/?status=published.
    - Filtering by ownership or user scope belongs in selectors, not here.
    - Apply via filterset_class on the view or set DEFAULT_FILTER_BACKENDS in settings.

Example:
    class PostFilter(filters.FilterSet):
        created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
        created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")

        class Meta:
            model = Post
            fields = ["status", "author"]
"""
