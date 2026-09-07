"""Verification routine.

BUKAN novelty. Routine-nya tetap dan dibekukan sebelum held-out:

  1. baca eligible claims;
  2. cek provenance;
  3. cek temporal validity;
  4. cek support span;
  5. cek fixed corroboration rule;
  6. kembalikan supported value atau abstain.

Routine ini tidak melakukan truth discovery: ia hanya memutuskan apakah
supported value cukup tersedia.
"""
from src.evidence.corroboration import corroborated_values
from src.evidence.support_span import has_valid_support_span
from src.processing.temporal_filter import filter_eligible_claims

RULE_VERSION = "v1"


def verify(claims, query_time, freshness_window_days=None, min_independent_sources=2):
    """Jalankan verification routine.

    Mengembalikan dict berisi value (None bila tidak ada supported value),
    jumlah evidence yang disentuh, dan jumlah artikel yang disentuh.
    """
    eligible = filter_eligible_claims(claims, query_time, freshness_window_days)
    supported = [c for c in eligible if has_valid_support_span(c)]
    values = corroborated_values(supported, min_independent_sources)

    articles = {
        c.get("url_or_reference")
        for c in supported
        if c.get("representation_type") != "structured" and c.get("url_or_reference")
    }

    return {
        "value": next(iter(values)) if len(values) == 1 else None,
        "evidence_claims_touched": len(eligible),
        "articles_touched": len(articles),
        "rule_version": RULE_VERSION,
    }


def resolve_action(action, verification_result):
    """Terapkan aturan 'Verify tanpa supported value -> Abstain'.

    Mengembalikan (final_action, returned_value, answered).
    """
    if action == "A":
        return "A", None, False
    if action == "D":
        return "D", (verification_result or {}).get("value"), True
    value = (verification_result or {}).get("value")
    if value is None:
        return "A", None, False
    return "V", value, True
