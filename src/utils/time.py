"""Utilitas waktu.

Seluruh perbandingan waktu di penelitian ini bersifat as-of query_time.
Timestamp naif (tanpa timezone) diperlakukan sebagai UTC agar perbandingan
tidak pernah gagal diam-diam.
"""
from datetime import datetime, timedelta, timezone

from dateutil import parser as _parser


def parse_ts(value):
    """Parse timestamp menjadi datetime aware. None tetap None."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        dt = _parser.parse(str(value))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def is_at_or_before(ts, query_time):
    """True bila ts tidak melampaui query_time.

    Timestamp None mengembalikan False: evidence tanpa waktu terbit tidak
    dapat dibuktikan mendahului query_time, jadi tidak boleh dipakai.
    """
    ts = parse_ts(ts)
    qt = parse_ts(query_time)
    if ts is None or qt is None:
        return False
    return ts <= qt


def within_freshness_window(ts, query_time, window_days):
    """True bila ts berada di dalam freshness window sebelum query_time.

    window_days None berarti atribut tidak kedaluwarsa (stable control).
    """
    if not is_at_or_before(ts, query_time):
        return False
    if window_days is None:
        return True
    return parse_ts(ts) >= parse_ts(query_time) - timedelta(days=window_days)
