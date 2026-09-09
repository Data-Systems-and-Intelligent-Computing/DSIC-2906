"""Ingest JADESTA raw scraped CSV ke raw zone.

Seluruh CSV di-ingest (bukan hanya candidate pool). JADESTA adalah structured
seed, BUKAN ground truth.
"""
import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

from pyarrow import fs as pafs

from src.acquisition.source_manifest import append_record
from src.utils.hashing import sha256_file
from src.utils.logging import get_logger

log = get_logger(__name__)

SOURCE_ID = "jadesta"
SOURCE_FAMILY = "jadesta"


def _load_dotenv_if_present(path=".env"):
    """Baca file .env sederhana dan isi os.environ kalau belum ada.

    Tidak pakai library tambahan (python-dotenv) supaya tetap sesuai
    requirements.txt yang sudah dibekukan.
    """
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def _s3_filesystem():
    """Bikin koneksi ke MinIO. Jalan dari laptop (bukan dari dalam Docker),
    jadi endpoint harus localhost, bukan nama service 'minio'.
    """
    access_key = os.environ.get("MINIO_ROOT_USER", "dsic2906")
    secret_key = os.environ.get("MINIO_ROOT_PASSWORD", "")
    return pafs.S3FileSystem(
        endpoint_override="localhost:9000",
        access_key=access_key,
        secret_key=secret_key,
        scheme="http",
    )


def snapshot_record(csv_path, fetched_at, raw_path, checksum):
    """Bangun record manifest untuk satu file CSV JADESTA."""
    return {
        "snapshot_id": f"{SOURCE_ID}-{checksum[:16]}",
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
        "checksum_sha256": checksum,
        "raw_path": raw_path,
        "content_type": "text/csv",
    }


def ingest(csv_path, raw_zone, manifest_path=None):
    """Upload satu file CSV JADESTA ke MinIO raw zone, lalu catat manifestnya."""
    csv_path = Path(csv_path)
    fetched_at = datetime.now(timezone.utc).isoformat()
    checksum = sha256_file(csv_path)

    # raw_zone contoh: s3://dsic2906/raw/jadesta -> jadi "dsic2906/raw/jadesta/nama.csv"
    bucket_and_key = raw_zone.replace("s3://", "").rstrip("/") + f"/{csv_path.name}"

    s3 = _s3_filesystem()
    with open(csv_path, "rb") as src, s3.open_output_stream(bucket_and_key) as dst:
        dst.write(src.read())

    record = snapshot_record(csv_path, fetched_at, raw_path=f"s3://{bucket_and_key}", checksum=checksum)
    if manifest_path:
        append_record(record, path=manifest_path)
    else:
        append_record(record)

    log.info(f"ingested {csv_path.name} -> s3://{bucket_and_key}")
    return record


def main():
    _load_dotenv_if_present()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="folder berisi CSV JADESTA mentah")
    parser.add_argument("--raw-zone", required=True, help="tujuan s3://bucket/prefix")
    parser.add_argument("--manifest", required=True, help="path file manifest CSV")
    args = parser.parse_args()

    input_dir = Path(args.input)
    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        log.warning(f"tidak ada file CSV ditemukan di {input_dir}")
        return

    for csv_path in csv_files:
        ingest(csv_path, args.raw_zone, manifest_path=args.manifest)

    log.info(f"selesai: {len(csv_files)} file CSV di-ingest ke {args.raw_zone}")


if __name__ == "__main__":
    main()