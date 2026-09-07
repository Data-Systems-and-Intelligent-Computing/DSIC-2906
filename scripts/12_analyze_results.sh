#!/usr/bin/env bash
# E3-E6: metrik, bootstrap, dan figure wajib.
# Risk selalu dilaporkan bersama coverage dan verification.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.evaluation.metrics    --input results/raw/route_log.jsonl --output results/processed/
python -m src.evaluation.bootstrap  --baseline B1 --treatment P1 --unit entity_id
python -m src.evaluation.plots      --output results/figures/
python -m src.evaluation.failure_analysis --min-cases 20 --output results/failure_cases/
