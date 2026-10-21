# Docs: https://docs.djangoproject.com/en/stable/topics/db/queries/
import datetime

from apps.monitor.models import Reading
from decimal import Decimal

from apps.monitor.utils import get_current_month_as_num


def get_latest_reading() -> Reading:
    latest_reading = Reading.objects.first()
    if latest_reading is None:
        raise ValueError("Reading cannot be none")
    return latest_reading

def get_total_consumption() -> Decimal:
    oldest = Reading.objects.all().order_by('recorded_at').first()
    latest = Reading.objects.all().order_by('-recorded_at').first()
    total_consumption = latest.reading - oldest.reading
    return total_consumption

def get_total_readings():
    return Reading.objects.count()

def get_total_cost_for_billing_cycle():
    year = 2026
    month = get_current_month_as_num()
    date = 25
    start = datetime.date(year, month-1, date)
    end = datetime.date(year, month, date)

    current_cost_per_kwh = 20

    readings = Reading.objects.filter(recorded_at__range=(start, end))
    oldest = readings.order_by('recorded_at').first()
    latest = readings.order_by('-recorded_at').first()
    total_consumption = latest.reading - oldest.reading
    return total_consumption * current_cost_per_kwh



