"""Akuisisi Wikipedia via MediaWiki API/export.

Peran: textual evidence. Ambil revisi yang berlaku pada source cutoff;
revisi setelah query_time tidak boleh dipakai sebagai evidence.
"""
from src.utils.logging import get_logger

log = get_logger(__name__)

SOURCE_ID = "wikipedia"
SOURCE_FAMILY = "wikimedia"

API_ENDPOINT = "https://id.wikipedia.org/w/api.php"


def fetch_revision_as_of(title, cutoff, user_agent):
    """Ambil revisi terakhir yang published_at <= cutoff.

    Memakai revisi terbaru akan memasukkan informasi yang belum ada pada
    query_time; itu temporal leakage.
    """
    raise NotImplementedError("Implementasikan pada H3-H4 (scripts/02_acquire_wikimedia.sh).")
