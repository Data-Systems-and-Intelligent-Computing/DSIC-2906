#!/usr/bin/env bash
# E5: latency query-time pada frozen snapshot.
# Latency crawling dan preprocessing TIDAK termasuk.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.evaluation.latency_benchmark \
  --policies B0,B1,B2,P1 \
  --warmup 2 \
  --repetitions 20 \
  --randomize-policy-order \
  --output results/raw/latency.jsonl
