"""Pengelompokan story lineage.

Satu press release yang di-repost tiga kali BUKAN tiga corroboration
independen. Lineage inilah yang mencegah syndication terhitung sebagai bukti
ganda.
"""
import re

from src.utils.hashing import sha256_text

_WS = re.compile(r"\s+")


def lineage_key(title, first_paragraph=None, canonical_url=None):
    """Kunci lineage untuk satu artikel.

    Urutan prioritas: canonical URL (bila publisher menyatakannya), lalu
    sidik jari judul + paragraf pertama.
    """
    if canonical_url:
        return sha256_text(canonical_url.strip().lower())[:16]
    basis = _WS.sub(" ", f"{title or ''} {first_paragraph or ''}").strip().lower()
    return sha256_text(basis)[:16]


def assign_lineage(articles):
    """Beri story_lineage_id pada setiap artikel."""
    out = []
    for article in articles:
        enriched = dict(article)
        enriched["story_lineage_id"] = lineage_key(
            article.get("title"),
            article.get("first_paragraph"),
            article.get("canonical_url"),
        )
        out.append(enriched)
    return out


def group_sizes(articles):
    """Ukuran tiap grup lineage; grup > 1 menandakan syndication."""
    counts = {}
    for article in articles:
        key = article.get("story_lineage_id")
        counts[key] = counts.get(key, 0) + 1
    return counts
