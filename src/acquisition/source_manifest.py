"""Pencatatan manifest sumber.

Tanpa manifest yang lengkap, gate "snapshots reproducible" dan "checksums
frozen" tidak dapat lulus.
"""
import csv
from pathlib import Path

MANIFEST_PATH = "data/manifests/source_manifest.csv"

FIELDS = [
    "snapshot_id",
    "source_id",
    "source_family",
    "representation_type",
    "url_or_reference",
    "publisher",
    "published_at",
    "fetched_at",
    "http_status",
    "discovery_query",
    "story_lineage_id",
    "checksum_sha256",
    "raw_path",
    "content_type",
]


def append_record(record, path=MANIFEST_PATH):
    missing = [f for f in ("snapshot_id", "source_id", "fetched_at", "checksum_sha256") if not record.get(f)]
    if missing:
        raise ValueError(f"Manifest kehilangan field wajib: {missing}")

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    exists = p.exists() and p.stat().st_size > 0
    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(record)


def read_manifest(path=MANIFEST_PATH):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return []
    with p.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
