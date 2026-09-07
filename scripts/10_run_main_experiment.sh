#!/usr/bin/env bash
# E3: B0/B1/B2/P1 pada Q1 held-out workload.
# Keempat policy WAJIB memakai snapshot, workload, gold, dan resource cap yang sama.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.evaluation.run_workload \
  --policies B0,B1,B2,P1 \
  --query Q1 \
  --heldout-only \
  --route-log results/raw/route_log.jsonl
