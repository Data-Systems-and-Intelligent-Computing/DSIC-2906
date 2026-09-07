#!/usr/bin/env bash
# E0: siapkan environment dan verifikasi stack dapat dibaca konsisten.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || { echo "ERROR: .env belum ada. Jalankan: cp .env.example .env"; exit 1; }

docker compose --env-file .env up -d
docker compose --env-file .env ps

echo "--- Verifikasi Trino melihat katalog Iceberg ---"
docker compose --env-file .env exec -T trino trino --execute "SHOW CATALOGS"

echo "--- Catat versi persis ke configs/environment.yaml dan docs/reproducibility.md ---"
docker compose --env-file .env images
