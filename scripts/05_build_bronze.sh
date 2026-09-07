#!/usr/bin/env bash
# E0/E1: Raw -> Bronze. Bronze mempertahankan bentuk sumber apa adanya.
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose --env-file .env exec -T trino trino -f sql/ddl/bronze_sources.sql
python -m src.processing.materialize_bronze --manifest data/manifests/source_manifest.csv
