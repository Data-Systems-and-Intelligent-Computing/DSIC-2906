"""Kontrak schema dan kelengkapan provenance."""
import json
from pathlib import Path

import pytest

from src.acquisition.crawl_news import validate_article
from src.processing.materialize_bronze import validate_snapshot

SCHEMA_DIR = Path("schemas")

EXPECTED_SCHEMAS = {
    "source_snapshot", "canonical_entity", "evidence_claim", "conflict_state",
    "query_request", "route_log", "gold_label", "raw_result",
}


def test_all_schemas_present_and_valid_json():
    found = {p.name.replace(".schema.json", "") for p in SCHEMA_DIR.glob("*.schema.json")}
    assert EXPECTED_SCHEMAS <= found
    for path in SCHEMA_DIR.glob("*.schema.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        assert doc["$schema"].startswith("https://json-schema.org/")
        assert doc["type"] == "object"
        assert doc["required"]


def test_evidence_claim_requires_provenance_and_extractor_version():
    doc = json.loads((SCHEMA_DIR / "evidence_claim.schema.json").read_text())
    for field in ("entity_id", "source_family", "published_or_observed_at", "extractor_version"):
        assert field in doc["required"]


def test_route_log_records_action_and_answered():
    doc = json.loads((SCHEMA_DIR / "route_log.schema.json").read_text())
    for field in ("policy", "action", "answered", "latency_ms"):
        assert field in doc["required"]
    assert doc["properties"]["action"]["enum"] == ["D", "V", "A"]


def test_snapshot_missing_checksum_is_rejected():
    record = {
        "snapshot_id": "s1", "source_id": "jadesta", "source_family": "jadesta",
        "representation_type": "structured", "url_or_reference": "x",
        "fetched_at": "2024-06-01T00:00:00Z", "http_status": 200, "raw_path": "p",
    }
    with pytest.raises(ValueError):
        validate_snapshot(record)
    record["checksum_sha256"] = "a" * 64
    assert validate_snapshot(record)


def test_article_without_published_at_is_rejected():
    article = {
        "url_or_reference": "https://x/1", "publisher": "X", "published_at": None,
        "fetched_at": "2024-06-01T00:00:00Z", "http_status": 200,
        "discovery_query": "q", "checksum_sha256": "b" * 64,
    }
    with pytest.raises(ValueError):
        validate_article(article)
