#!/usr/bin/env bash
# Minggu 2: ekspor formulir anotasi gold.
# Formulir TIDAK boleh memuat keluaran policy apa pun.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.annotation.export_gold_form --output data/annotations/gold_requests.csv
echo "Ekspor selesai. Second annotation: 20-25% request, dan >=20% / ~100 news claim."
