"""Akuisisi berita pariwisata yang tertarget.

Bukan crawling seluruh web: publisher dan candidate entity harus sudah
dibekukan lebih dulu. Untuk setiap artikel wajib tercatat URL, publisher,
published_at, fetched_at, http_status, discovery query, checksum, dan
story lineage.
"""
from src.utils.logging import get_logger

log = get_logger(__name__)

REQUIRED_FIELDS = (
    "url_or_reference",
    "publisher",
    "published_at",
    "fetched_at",
    "http_status",
    "discovery_query",
    "checksum_sha256",
)


def validate_article(record):
    """Artikel tanpa published_at tidak dapat dibuktikan mendahului query_time
    sehingga tidak akan pernah temporally eligible."""
    missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
    if missing:
        raise ValueError(f"Artikel kehilangan field wajib: {missing}")
    return True


def crawl(publishers, entities, user_agent, delay_seconds=2, respect_robots=True):
    raise NotImplementedError("Implementasikan pada H3-H4 (scripts/03_acquire_news.sh).")
