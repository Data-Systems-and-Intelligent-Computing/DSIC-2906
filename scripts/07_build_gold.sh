#!/usr/bin/env bash
# E2: Silver -> Gold. C_S, C_SU, query workload, gold labels, route log.
# Jalankan HANYA setelah conflict/freshness/routing rule dibekukan.
set -euo pipefail
cd "$(dirname "$0")/.."
for f in sql/ddl/gold_conflict_states.sql sql/ddl/gold_query_workload.sql \
         sql/ddl/gold_gold_labels.sql sql/ddl/gold_route_log.sql; do
  docker compose --env-file .env exec -T trino trino -f "$f"
done
python -m src.processing.materialize_gold --states
for v in sql/views/*.sql; do
  docker compose --env-file .env exec -T trino trino -f "$v"
done
