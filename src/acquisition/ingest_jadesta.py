"""Ingest JADESTA raw scraped CSV ke raw zone.

Seluruh CSV di-ingest (bukan hanya candidate pool). JADESTA adalah structured
seed, BUKAN ground truth.
"""
from src.utils.hashing import sha256_file
from src.utils.logging import get_logger

log = get_logger(__name__)

SOURCE_ID = "jadesta"
SOURCE_FAMILY = "jadesta"


def snapshot_record(csv_path, fetched_at, raw_path):
    """Bangun record manifest untuk satu file CSV JADESTA."""
    return {
        "snapshot_id": f"{SOURCE_ID}-{sha256_file(csv_path)[:16]}",
        "source_id": SOURCE_ID,
        "source_family": SOURCE_FAMILY,
        "representation_type": "structured",
        "url_or_reference": str(csv_path),
        "publisher": None,
        "published_at": None,
        "fetched_at": fetched_at,
        "http_status": 200,
        "discovery_query": "bulk_scraped_csv",
        "story_lineage_id": None,
        "checksum_sha256": sha256_file(csv_path),
        "raw_path": raw_path,
        "content_type": "text/csv",
    }


def ingest(csv_path, raw_zone):
    raise NotImplementedError("Implementasikan pada H1-H2 (scripts/01_ingest_jadesta.sh).")
