from datetime import date, datetime, time, timedelta, timezone

# The dashboard's business day is Beijing time (UTC+8). No DST, so a fixed
# offset is sufficient and avoids a tzdata dependency in slim images.
BEIJING_TZ = timezone(timedelta(hours=8))


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


def now_beijing() -> datetime:
    return datetime.now(BEIJING_TZ)


def today_beijing() -> date:
    return now_beijing().date()


def beijing_day_start_utc_naive(day: date) -> datetime:
    """Convert 00:00 Beijing on `day` to a naive UTC datetime."""
    return datetime.combine(day, time.min, tzinfo=BEIJING_TZ).astimezone(timezone.utc).replace(tzinfo=None)


def beijing_range_utc_naive(start: date, end_exclusive: date) -> tuple[datetime, datetime]:
    return beijing_day_start_utc_naive(start), beijing_day_start_utc_naive(end_exclusive)

