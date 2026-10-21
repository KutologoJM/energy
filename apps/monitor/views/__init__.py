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
from apps.monitor.selectors import get_latest_reading, get_total_consumption, get_total_readings, get_total_cost_for_billing_cycle
from apps.monitor.services.generators import create_reading
from apps.monitor.utils import get_current_month

def index(request):
    context = {}
    latest_reading = get_latest_reading()
    lr_time = latest_reading.recorded_at.time()
    lr_date = latest_reading.recorded_at.date()
    context["latest_reading"] = latest_reading
    context["lr_date"] = lr_date
    context["lr_time"] = lr_time
    context["total_consumption"] = get_total_consumption()
    context["total_readings"] = get_total_readings()
    context["total_cost"] = get_total_cost_for_billing_cycle()
    context["current_month"] = get_current_month()
    return render(request, "pages/index.html", context=context)


def process_new_reading(request):
    context = {}
    if request.method == "POST":
        new_reading = request.POST.get("reading")
        reading_timestamp = request.POST.get("timestamp")
        create_reading(reading=new_reading, timestamp=reading_timestamp)

        latest_reading = get_latest_reading()
        lr_time = latest_reading.recorded_at.time()
        lr_date = latest_reading.recorded_at.date()
        context["latest_reading"] = latest_reading
        context["lr_date"] = lr_date
        context["lr_time"] = lr_time
        context["total_consumption"] = get_total_consumption()
        context["total_readings"] = get_total_readings()
        context["total_cost"] = get_total_cost_for_billing_cycle()
        context["current_month"] = get_current_month()
    return render(request, "components/stats.html", context=context)
