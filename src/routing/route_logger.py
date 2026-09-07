"""Penulisan route log (JSONL).

Gate penelitian mensyaratkan route log dan evidence-touched tersimpan; ini
bukti mentah untuk risk, coverage, DCR/BDCR, dan cost.
"""
import json
from pathlib import Path

DEFAULT_PATH = "results/raw/route_log.jsonl"

REQUIRED_FIELDS = ("request_id", "policy", "conflict_label", "action", "answered", "latency_ms")


def write_route(record, path=DEFAULT_PATH):
    missing = [f for f in REQUIRED_FIELDS if f not in record]
    if missing:
        raise ValueError(f"Route log kehilangan field wajib: {missing}")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def read_routes(path=DEFAULT_PATH):
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
