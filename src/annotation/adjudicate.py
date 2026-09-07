"""Adjudikasi disagreement.

Wajib selesai sebelum final evaluation (gate Minggu 2).
"""
import csv
from pathlib import Path

LOG_PATH = "data/annotations/adjudication_log.csv"

FIELDS = [
    "request_id",
    "annotator_a",
    "label_a",
    "annotator_b",
    "label_b",
    "adjudicator",
    "final_label",
    "reason",
    "adjudicated_at",
]


def find_disagreements(first, second, key="request_id", label="outcome"):
    """Pasangkan anotasi pertama dan kedua, kembalikan yang berbeda."""
    index = {r[key]: r for r in first}
    out = []
    for row in second:
        base = index.get(row.get(key))
        if base and base.get(label) != row.get(label):
            out.append({"request_id": row[key], "label_a": base.get(label), "label_b": row.get(label)})
    return out


def append_decision(record, path=LOG_PATH):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    exists = p.exists() and p.stat().st_size > 0
    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(record)
