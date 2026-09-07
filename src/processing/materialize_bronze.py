"""Raw -> Bronze.

Bronze mempertahankan bentuk sumber apa adanya beserta metadata akuisisi.
Normalisasi TIDAK dilakukan di sini; itu pekerjaan Silver.
"""
from src.utils.logging import get_logger

log = get_logger(__name__)

REQUIRED_FIELDS = (
    "snapshot_id",
    "source_id",
    "source_family",
    "representation_type",
    "url_or_reference",
    "fetched_at",
    "http_status",
    "checksum_sha256",
    "raw_path",
)


def validate_snapshot(record):
    """Provenance yang tidak lengkap membuat gate 'snapshots reproducible' gagal."""
    missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
    if missing:
        raise ValueError(f"Snapshot {record.get('snapshot_id')} kehilangan field: {missing}")
    return True


def materialize(snapshots, table="iceberg.bronze.sources"):
    raise NotImplementedError("Implementasikan dengan Spark pada H5 (scripts/05_build_bronze.sh).")
