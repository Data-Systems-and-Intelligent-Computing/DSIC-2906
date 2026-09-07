#!/usr/bin/env bash
# Minggu 4: reproduksi dari environment bersih.
# Gate artikel: artifact mereproduksi satu main table dan satu main figure.
set -euo pipefail
cd "$(dirname "$0")/.."

docker compose --env-file .env down -v
bash scripts/00_bootstrap_environment.sh
bash scripts/05_build_bronze.sh
bash scripts/06_build_silver.sh
bash scripts/07_build_gold.sh
bash scripts/10_run_main_experiment.sh
bash scripts/12_analyze_results.sh

echo "Bandingkan hasil dengan results v1 dan laporkan selisihnya."
