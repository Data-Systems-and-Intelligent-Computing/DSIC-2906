.PHONY: help setup up down ps test lint \
        ingest acquire freeze bronze silver gold \
        annotate heldout experiment latency analyze reproduce

help:
	@grep -E '^[a-z-]+:' Makefile | sed 's/:.*//' | tr '\n' ' '; echo

# --- environment ---
setup:
	python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
up:
	docker compose --env-file .env up -d
down:
	docker compose --env-file .env down
ps:
	docker compose --env-file .env ps

test:
	pytest -q
lint:
	ruff check src tests

# --- Minggu 1: acquisition + minimum viable lakehouse (E0/E1) ---
ingest:
	bash scripts/01_ingest_jadesta.sh
acquire:
	bash scripts/02_acquire_wikimedia.sh
	bash scripts/03_acquire_news.sh
freeze:
	bash scripts/04_freeze_sources.sh
bronze:
	bash scripts/05_build_bronze.sh
silver:
	bash scripts/06_build_silver.sh

# --- Minggu 2: gold + annotation + held-out freeze (E2) ---
gold:
	bash scripts/07_build_gold.sh
annotate:
	bash scripts/08_export_annotation.sh
heldout:
	bash scripts/09_freeze_heldout.sh

# --- Minggu 3: main experiment (E3-E6) ---
experiment:
	bash scripts/10_run_main_experiment.sh
latency:
	bash scripts/11_run_latency_benchmark.sh
analyze:
	bash scripts/12_analyze_results.sh

# --- Minggu 4: reproduction ---
reproduce:
	bash scripts/13_reproduce_main.sh
