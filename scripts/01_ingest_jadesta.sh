#!/usr/bin/env bash
# E0: ingest SELURUH JADESTA CSV ke raw zone (bukan hanya candidate pool).
# JADESTA adalah structured seed, bukan ground truth.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.acquisition.ingest_jadesta \
  --input "data/raw/jadesta" \
  --raw-zone "s3://${MINIO_BUCKET:-dsic2906}/raw/jadesta" \
  --manifest data/manifests/source_manifest.csv
