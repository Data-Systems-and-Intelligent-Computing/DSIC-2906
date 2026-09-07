"""Ekspor request untuk dianotasi.

Formulir sengaja TIDAK memuat keluaran policy mana pun: anotator menilai
as-of query_time berdasarkan evidence, bukan berdasarkan tebakan sistem.
"""
import csv
from pathlib import Path

OUTPUT = "data/annotations/gold_requests.csv"

FIELDS = [
    "request_id",
    "entity_id",
    "canonical_name",
    "attribute",
    "attribute_class",
    "query_time",
    "evidence_refs",
    "outcome",
    "accepted_values",
    "annotator_id",
    "annotated_at",
    "is_second_annotation",
    "note",
]

# Kolom yang tidak boleh muncul di formulir anotasi.
FORBIDDEN_FIELDS = {"action", "policy", "returned_value", "conflict_label", "correct"}


def export(requests, path=OUTPUT):
    leaked = FORBIDDEN_FIELDS & set().union(*(set(r) for r in requests)) if requests else set()
    if leaked:
        raise ValueError(f"Formulir anotasi tidak boleh memuat keluaran sistem: {sorted(leaked)}")

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in requests:
            writer.writerow(r)
    return path
