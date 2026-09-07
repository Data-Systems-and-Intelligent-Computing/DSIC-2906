#!/usr/bin/env bash
# E1: Bronze -> Silver. Normalisasi, entity linking, claim extraction, support span.
set -euo pipefail
cd "$(dirname "$0")/.."
for f in sql/ddl/silver_entities.sql sql/ddl/silver_evidence_claims.sql; do
  docker compose --env-file .env exec -T trino trino -f "$f"
done
python -m src.processing.materialize_silver --stage entities
python -m src.processing.materialize_silver --stage claims

echo "--- Coverage audit: dasar pemilihan atribut final (H7) ---"
docker compose --env-file .env exec -T trino trino -f sql/queries/coverage_summary.sql
