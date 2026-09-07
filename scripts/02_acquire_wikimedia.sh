#!/usr/bin/env bash
# E0: akuisisi Wikidata + Wikipedia untuk candidate pool.
# Keduanya berbagi family lineage `wikimedia`: bukan dua sumber independen.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.acquisition.fetch_wikidata  --pool data/manifests/candidate_pool.csv
python -m src.acquisition.fetch_wikipedia --pool data/manifests/candidate_pool.csv
