#!/usr/bin/env bash
# E0 langkah terakhir: bekukan source cutoff (akhir Minggu 1).
# Setelah ini tidak boleh ada sumber/publisher baru masuk held-out evaluation.
set -euo pipefail
cd "$(dirname "$0")/.."

CUTOFF="${1:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
echo "source_cutoff: \"${CUTOFF}\"" > data/manifests/source_cutoff.yaml
echo "frozen_at: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> data/manifests/source_cutoff.yaml
sha256sum data/manifests/*.csv > data/checksums/manifests.sha256 2>/dev/null \
  || shasum -a 256 data/manifests/*.csv > data/checksums/manifests.sha256
echo "Source cutoff dibekukan pada ${CUTOFF}"
