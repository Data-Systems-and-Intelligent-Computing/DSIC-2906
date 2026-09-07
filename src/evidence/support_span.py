"""Validasi supporting span.

Aturan penelitian: setiap claim unstructured wajib punya span yang benar-benar
mendukung normalized_value. Claim tanpa span valid adalah *unsupported claim*
dan TIDAK boleh dihitung sebagai corroboration.
"""
MIN_CHARS = 20
MAX_CHARS = 600

UNSTRUCTURED_TYPES = {"unstructured_text", "semi_structured_text"}


def requires_support_span(claim):
    return claim.get("representation_type") in UNSTRUCTURED_TYPES


def has_valid_support_span(claim, min_chars=MIN_CHARS, max_chars=MAX_CHARS):
    """Apakah claim ini punya span pendukung yang sah?

    Claim structured tidak memerlukan span sehingga selalu True.
    """
    if not requires_support_span(claim):
        return True

    span = claim.get("support_span") or {}
    text = (span.get("text") or "").strip()
    if not text:
        return False
    if not (min_chars <= len(text) <= max_chars):
        return False

    value = (claim.get("normalized_value") or "").strip()
    if not value:
        return False

    # Pemeriksaan minimum: span harus benar-benar menyebut nilai yang diklaim.
    # Ekstraktor yang lebih kaya boleh memperketat ini, tidak boleh melonggarkan.
    return value.lower() in text.lower()


def mark_support_validity(claims):
    """Kembalikan salinan claims dengan field support_valid terisi."""
    out = []
    for claim in claims:
        enriched = dict(claim)
        enriched["support_valid"] = has_valid_support_span(claim)
        out.append(enriched)
    return out
