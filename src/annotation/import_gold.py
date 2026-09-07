"""Impor label gold hasil anotasi."""
import csv
from pathlib import Path

VALID_OUTCOMES = {"accepted_value", "unresolved_unknown", "not_applicable"}


def load(path="data/annotations/gold_requests.csv"):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return []
    with p.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row.get("outcome") and row["outcome"] not in VALID_OUTCOMES:
            raise ValueError(f"Outcome tidak valid pada {row.get('request_id')}: {row['outcome']}")
    return rows


def split_annotations(rows):
    """Pisahkan anotasi pertama dan kedua untuk perhitungan agreement."""
    first = [r for r in rows if str(r.get("is_second_annotation", "")).lower() not in ("true", "1")]
    second = [r for r in rows if str(r.get("is_second_annotation", "")).lower() in ("true", "1")]
    return first, second
