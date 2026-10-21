"""
Stateless utility functions with no database access and no side effects.

Docs: https://docs.python.org/3/library/functions.html

Rules:
    - Functions here must be pure: same input always produces the same output.
    - No database access — if a helper needs the DB, it belongs in selectors.
    - No side effects — if a helper sends email or writes files, it belongs in external.py.
    - Utilities should be generic enough to be used across multiple apps.

Example:
    def build_full_name(first_name, last_name):
        return f"{first_name} {last_name}".strip()

    def truncate(text, max_length=100, suffix="..."):
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
"""

from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def generate_datetime_from_raw_data(raw_date, raw_time):
    d = datetime.strptime(raw_date, "%Y-%m-%d").date()
    t = datetime.strptime(raw_time, "%H:%M:%S").time()
    naive_dt = datetime.combine(d, t)
    aware_dt = timezone.make_aware(naive_dt)
    return aware_dt


def generate_datetime_from_timestamp(timestamp):
    naive_dt = parse_datetime(timestamp)
    if naive_dt is None:
        raise ValueError("Cannot be None")
    aware_dt = timezone.make_aware(naive_dt)
    return aware_dt


def get_current_month():
    import calendar
    curr_month_as_num = datetime.today().month
    month_name = calendar.month_name[curr_month_as_num]
    return month_name

def get_current_month_as_num():
    return datetime.today().month
