#!/usr/bin/env bash
# E0: akuisisi berita tertarget. BUKAN crawling seluruh web.
# Publisher dan candidate entity harus sudah dibekukan lebih dulu.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.acquisition.crawl_news \
  --publishers configs/sources.yaml \
  --pool data/manifests/candidate_pool.csv \
  --manifest data/manifests/news_manifest.csv \
  --lineage data/manifests/story_lineage.csv
