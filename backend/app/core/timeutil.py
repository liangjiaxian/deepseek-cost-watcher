from datetime import datetime, timezone


def utc_iso(value: datetime | None) -> str | None:
    """Serialize a stored (naive UTC) datetime with an explicit UTC offset.

    Naive timestamps from the database are UTC; without a trailing `Z` the
    browser parses them as local time and displays them 8 hours behind in
    UTC+8. Aware datetimes are converted to UTC first.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
