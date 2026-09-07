"""Perhitungan sumber independen.

Jumlah halaman bukan jumlah bukti. Dua reduksi wajib dilakukan sebelum
menghitung corroboration:

  1. story lineage - satu press release yang di-repost N kali tetap SATU;
  2. source family - Wikidata dan Wikipedia berbagi family `wikimedia`.
"""
from src.utils.config import load_config


def independence_key(claim):
    """Kunci yang menyatakan 'satu suara independen'.

    Story lineage lebih kuat daripada family: bila dua publisher berbeda
    memuat ulang satu origin, keduanya tetap satu suara.
    """
    lineage = claim.get("story_lineage_id")
    if lineage:
        return ("lineage", lineage)
    return ("family", claim.get("source_family") or claim.get("source_id"))


def count_independent_sources(claims):
    return len({independence_key(c) for c in claims})


def independent_claims(claims):
    """Satu claim wakil per sumber independen, mempertahankan urutan masukan."""
    seen, out = set(), []
    for claim in claims:
        key = independence_key(claim)
        if key not in seen:
            seen.add(key)
            out.append(claim)
    return out


def corroborated_values(claims, min_independent_sources=None):
    """Nilai yang didukung minimal N sumber independen."""
    if min_independent_sources is None:
        rules = load_config("conflict_rules")
        min_independent_sources = rules["corroboration"]["min_independent_sources"]

    by_value = {}
    for claim in claims:
        value = claim.get("normalized_value")
        if value is None:
            continue
        by_value.setdefault(value, set()).add(independence_key(claim))

    return {v for v, keys in by_value.items() if len(keys) >= min_independent_sources}
