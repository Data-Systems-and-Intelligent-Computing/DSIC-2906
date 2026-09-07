"""Pelabelan C_S / C_SU."""
from src.evidence.conflict_state import CLEAN, INSUFFICIENT, MODERATE, SEVERE, build_state, classify

QT = "2024-06-01T00:00:00Z"
SPAN_TUTUP = "Pengelola menyatakan kawasan ini tutup sementara sampai pemberitahuan lanjut."


def structured(value, source):
    return {
        "representation_type": "structured",
        "normalized_value": value,
        "source_id": source,
        "source_family": source,
        "published_or_observed_at": "2024-01-01T00:00:00Z",
    }


def news(value, source, ts, span=SPAN_TUTUP, lineage=None):
    return {
        "representation_type": "unstructured_text",
        "normalized_value": value,
        "source_id": source,
        "source_family": source,
        "story_lineage_id": lineage,
        "published_or_observed_at": ts,
        "support_span": {"text": span},
        "url_or_reference": f"https://{source}/a",
    }


def test_no_evidence_is_insufficient():
    assert classify([]) == INSUFFICIENT


def test_agreement_is_clean():
    assert classify([structured("buka", "jadesta"), structured("buka", "wikidata")]) == CLEAN


def test_one_corroborated_value_is_moderate():
    claims = [
        structured("buka", "jadesta"),
        news("tutup", "pubA", QT),
        news("tutup", "pubB", QT),
    ]
    assert classify(claims, min_independent_sources=2) == MODERATE


def test_conflict_without_corroboration_is_severe():
    claims = [structured("buka", "jadesta"), news("tutup", "pubA", QT)]
    assert classify(claims, min_independent_sources=2) == SEVERE


def test_cs_ignores_news_entirely():
    claims = [structured("buka", "jadesta"), news("tutup", "pubA", QT)]
    state = build_state(claims, QT, "C_S")
    assert state["label"] == CLEAN
    assert state["news_claims_eligible"] == 0


def test_csu_sees_the_same_news_and_changes_label():
    claims = [structured("buka", "jadesta"), news("tutup", "pubA", QT)]
    state = build_state(claims, QT, "C_SU")
    assert state["label"] == SEVERE
    assert state["news_claims_eligible"] == 1


def test_csu_records_why_news_was_excluded():
    claims = [
        structured("buka", "jadesta"),
        news("tutup", "pubA", "2024-07-01T00:00:00Z"),   # setelah query time
        news("tutup", "pubB", "2020-01-01T00:00:00Z"),   # basi
        news("tutup", "pubC", QT, span="pendek"),        # span tidak valid
    ]
    state = build_state(claims, QT, "C_SU", freshness_window_days=180)
    assert state["news_claims_excluded_after_query_time"] == 1
    assert state["news_claims_excluded_stale"] == 1
    assert state["news_claims_excluded_unsupported"] == 1
    assert state["news_claims_eligible"] == 0
    # Tanpa berita eligible, C_SU kembali sama dengan C_S.
    assert state["label"] == CLEAN


def test_invalid_state_type_rejected():
    import pytest

    with pytest.raises(ValueError):
        build_state([], QT, "C_X")
