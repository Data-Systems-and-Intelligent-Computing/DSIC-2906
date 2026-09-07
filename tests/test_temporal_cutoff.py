"""Aturan keras: tidak ada evidence setelah query_time."""
from src.processing.temporal_filter import filter_eligible_claims, is_eligible
from src.utils.time import is_at_or_before, within_freshness_window

QT = "2024-06-01T00:00:00Z"


def claim(ts):
    return {"published_or_observed_at": ts, "normalized_value": "buka"}


def test_evidence_after_query_time_is_rejected():
    assert not is_eligible(claim("2024-06-02T00:00:00Z"), QT)


def test_evidence_at_query_time_is_accepted():
    assert is_eligible(claim(QT), QT)


def test_claim_without_timestamp_is_never_eligible():
    # Tanpa waktu terbit, tidak dapat dibuktikan mendahului query_time.
    assert not is_eligible(claim(None), QT)
    assert not is_at_or_before(None, QT)


def test_naive_timestamp_treated_as_utc_not_crash():
    assert is_at_or_before("2024-05-31T23:00:00", QT)


def test_freshness_window_excludes_stale_evidence():
    assert within_freshness_window("2024-05-01T00:00:00Z", QT, 180)
    assert not within_freshness_window("2023-01-01T00:00:00Z", QT, 180)


def test_null_window_means_never_stale():
    # Stable-control attribute tidak kedaluwarsa.
    assert within_freshness_window("2019-01-01T00:00:00Z", QT, None)


def test_exclusion_reasons_are_separated():
    claims = [
        claim("2024-06-05T00:00:00Z"),  # setelah query time
        claim("2020-01-01T00:00:00Z"),  # basi
        claim("2024-05-15T00:00:00Z"),  # eligible
    ]
    eligible, reasons = filter_eligible_claims(claims, QT, 180, return_reasons=True)
    assert len(eligible) == 1
    assert reasons == {"after_query_time": 1, "stale": 1}
