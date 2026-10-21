from apps.monitor.models import Reading
from apps.monitor.utils import generate_datetime_from_raw_data, generate_datetime_from_timestamp


def create_reading(reading, date=None, time=None, timestamp=None):
    if timestamp:
        recorded_at = generate_datetime_from_timestamp(timestamp)
    elif date and time:
        recorded_at = generate_datetime_from_raw_data(raw_date=date, raw_time=time)
    else:
        raise ValueError("Unsupported date time entry")
    Reading.objects.create(
        reading=reading,
        recorded_at=recorded_at
    )
