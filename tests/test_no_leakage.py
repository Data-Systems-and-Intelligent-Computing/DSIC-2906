"""Pertahanan terhadap leakage: temporal, routing, dan anotasi."""
import pytest

from src.annotation.export_gold_form import export
from src.evidence.conflict_state import build_state
from src.utils.config import load_config

QT = "2024-06-01T00:00:00Z"


def test_freshness_and_rules_are_marked_frozen():
    for name in ("conflict_rules", "freshness", "routing", "entity_linking", "claim_extraction"):
        cfg = load_config(name)
        assert cfg.get("freeze_before_heldout") is True, f"{name} tidak ditandai beku"


def test_hard_rule_no_evidence_after_query_time_is_enabled():
    assert load_config("freshness")["temporal"]["hard_rule_no_evidence_after_query_time"] is True


def test_future_evidence_never_enters_augmented_state():
    future = {
        "representation_type": "unstructured_text",
        "normalized_value": "tutup",
        "source_id": "pubA",
        "source_family": "pubA",
        "published_or_observed_at": "2025-01-01T00:00:00Z",
        "support_span": {"text": "Kawasan wisata ini tutup sementara menurut pengelola setempat."},
    }
    state = build_state([future], QT, "C_SU")
    assert state["news_claims_eligible"] == 0
    assert state["news_claims_excluded_after_query_time"] == 1


def test_annotation_form_rejects_system_output(tmp_path):
    # Anotator tidak boleh melihat keputusan policy.
    leaking = [{"request_id": "1", "entity_id": "e1", "action": "D", "correct": True}]
    with pytest.raises(ValueError):
        export(leaking, path=tmp_path / "gold.csv")


def test_annotation_form_accepts_clean_requests(tmp_path):
    clean = [{"request_id": "1", "entity_id": "e1", "attribute": "operational_status",
              "query_time": QT, "attribute_class": "time_sensitive"}]
    path = export(clean, path=tmp_path / "gold.csv")
    assert path.exists()


def test_bootstrap_unit_is_entity_not_row():
    assert load_config("experiment")["units"]["bootstrap_resampling_unit"] == "entity_id"


def test_candidate_pool_selection_independent_of_p1():
    pool = load_config("experiment")["candidate_pool"]
    assert pool["selection_must_not_depend_on_p1_output"] is True
    assert pool["freeze_before_external_enrichment"] is True
