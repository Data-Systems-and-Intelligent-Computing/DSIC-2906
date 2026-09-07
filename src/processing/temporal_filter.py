"""Penyaringan temporal.

Aturan keras penelitian: tidak ada evidence dengan waktu terbit melampaui
query_time. Ini pertahanan utama terhadap temporal leakage.
"""
from src.utils.time import is_at_or_before, within_freshness_window


def is_eligible(claim, query_time, freshness_window_days=None):
    ts = claim.get("published_or_observed_at")
    if not is_at_or_before(ts, query_time):
        return False
    return within_freshness_window(ts, query_time, freshness_window_days)


def filter_eligible_claims(claims, query_time, freshness_window_days=None, return_reasons=False):
    """Saring claim yang temporally eligible.

    return_reasons=True juga mengembalikan hitungan alasan eksklusi, yang
    diperlukan agar analisis value-of-news dapat membedakan "berita tidak ada"
    dari "berita ada tetapi tidak eligible".
    """
    eligible = []
    reasons = {"after_query_time": 0, "stale": 0}

    for claim in claims:
        ts = claim.get("published_or_observed_at")
        if not is_at_or_before(ts, query_time):
            reasons["after_query_time"] += 1
            continue
        if not within_freshness_window(ts, query_time, freshness_window_days):
            reasons["stale"] += 1
            continue
        eligible.append(claim)

    return (eligible, reasons) if return_reasons else eligible
