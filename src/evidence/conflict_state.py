"""Pembentukan conflict state C_S dan C_SU.

Label: CLEAN | MODERATE | SEVERE | INSUFFICIENT (configs/conflict_rules.yaml).
Rule dibekukan sebelum held-out dan tidak boleh diubah setelah melihat hasil.
"""
from src.evidence.corroboration import corroborated_values, count_independent_sources
from src.evidence.support_span import has_valid_support_span
from src.processing.temporal_filter import filter_eligible_claims

CLEAN = "CLEAN"
MODERATE = "MODERATE"
SEVERE = "SEVERE"
INSUFFICIENT = "INSUFFICIENT"

LABELS = (CLEAN, MODERATE, SEVERE, INSUFFICIENT)

RULE_VERSION = "v1"


def classify(claims, min_independent_sources=2):
    """Beri label conflict pada sekumpulan claim yang SUDAH eligible.

    Penyaringan temporal dan support dilakukan di build_state, bukan di sini,
    agar aturan pelabelan dapat diuji terpisah dari aturan kelayakan.
    """
    if not claims:
        return INSUFFICIENT

    values = {c.get("normalized_value") for c in claims if c.get("normalized_value") is not None}
    if not values:
        return INSUFFICIENT
    if len(values) == 1:
        return CLEAN

    supported = corroborated_values(claims, min_independent_sources)
    # Tepat satu nilai yang corroborated -> ada dasar untuk verifikasi.
    # Nol atau lebih dari satu -> tidak ada dasar memilih; abstain.
    return MODERATE if len(supported) == 1 else SEVERE


def build_state(
    claims,
    query_time,
    state_type,
    freshness_window_days=None,
    min_independent_sources=2,
):
    """Bangun satu conflict state lengkap dengan alasan eksklusi.

    state_type 'C_S' membuang seluruh claim berita; 'C_SU' menyertakan berita
    yang temporally eligible. Perbedaan inilah yang diukur sebagai value-of-news.
    """
    if state_type not in ("C_S", "C_SU"):
        raise ValueError("state_type harus 'C_S' atau 'C_SU'")

    structured = [c for c in claims if c.get("representation_type") == "structured"]
    news = [c for c in claims if c.get("representation_type") != "structured"]

    excluded = {
        "after_query_time": 0,
        "stale": 0,
        "unsupported": 0,
        "syndicated": 0,
    }

    if state_type == "C_S":
        eligible_news = []
    else:
        temporal_ok, reasons = filter_eligible_claims(
            news, query_time, freshness_window_days, return_reasons=True
        )
        excluded["after_query_time"] = reasons["after_query_time"]
        excluded["stale"] = reasons["stale"]

        supported = [c for c in temporal_ok if has_valid_support_span(c)]
        excluded["unsupported"] = len(temporal_ok) - len(supported)

        # Syndication tidak dibuang dari evidence, tetapi tidak menambah
        # kemerdekaan sumber. Dicatat agar dapat dilaporkan.
        independent = count_independent_sources(supported)
        excluded["syndicated"] = max(0, len(supported) - independent)
        eligible_news = supported

    eligible = structured + eligible_news
    label = classify(eligible, min_independent_sources)
    supported_values = corroborated_values(eligible, min_independent_sources)

    return {
        "query_time": query_time,
        "state_type": state_type,
        "label": label,
        "eligible_claim_count": len(eligible),
        "distinct_normalized_values": len(
            {c.get("normalized_value") for c in eligible if c.get("normalized_value") is not None}
        ),
        "independent_source_count": count_independent_sources(eligible),
        "corroborated_value": next(iter(supported_values)) if len(supported_values) == 1 else None,
        "news_claims_eligible": len(eligible_news),
        "news_claims_excluded_after_query_time": excluded["after_query_time"],
        "news_claims_excluded_stale": excluded["stale"],
        "news_claims_excluded_unsupported": excluded["unsupported"],
        "news_claims_excluded_syndicated": excluded["syndicated"],
        "rule_version": RULE_VERSION,
    }
