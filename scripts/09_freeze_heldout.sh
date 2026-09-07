#!/usr/bin/env bash
# Minggu 2 gate: bekukan held-out sebelum eksperimen utama.
# Setelah ini, rule apa pun tidak boleh diubah (routing leakage).
set -euo pipefail
cd "$(dirname "$0")/.."

python -m src.annotation.import_gold --validate
python -m src.annotation.adjudicate --check-complete

shasum -a 256 \
  configs/conflict_rules.yaml configs/freshness.yaml configs/routing.yaml \
  configs/entity_linking.yaml configs/claim_extraction.yaml \
  data/manifests/query_workload.csv data/annotations/gold_requests.csv \
  > data/checksums/heldout_freeze.sha256
echo "Held-out dibekukan. Checksum rule + workload + gold tersimpan."
