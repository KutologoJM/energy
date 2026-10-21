"""
DRF API views coordinating request handling for JSON endpoints.

Docs: https://www.django-rest-framework.org/api-guide/views/

Rules:
    - Views are thin coordinators — no business logic, no raw ORM queries.
    - Call selectors for reads, services for writes.
    - Catch domain exceptions from exceptions.py and map them to DRF Response status codes.
    - Never pass request objects into services or selectors.

Example:
    class PostListCreateView(generics.GenericAPIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            serializer = PostCreateInputSerializer(data=request.data, user=request.user)
            serializer.is_valid(raise_exception=True)
            try:
                post = create_post(user=request.user, **serializer.validated_data)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=400)
            return Response(PostOutputSerializer(post).data, status=201)
"""
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "pages/index.html", context=context)