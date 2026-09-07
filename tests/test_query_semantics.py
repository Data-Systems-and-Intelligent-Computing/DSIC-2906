"""Semantik SQL: cutoff as-of query_time dan isolasi C_S vs C_SU."""
from pathlib import Path

SQL = Path("sql")


def read(rel):
    return (SQL / rel).read_text(encoding="utf-8")


def test_all_query_files_present():
    for name in (
        "queries/Q1_entity_attribute_lookup.sql",
        "queries/Q2_multi_attribute_profile.sql",
        "queries/Q3_time_sensitive_status.sql",
    ):
        assert (SQL / name).exists()


def test_every_query_applies_query_time_cutoff():
    for path in (SQL / "queries").glob("Q*.sql"):
        sql = path.read_text(encoding="utf-8")
        assert "published_or_observed_at <=" in sql, f"{path.name} tanpa cutoff as-of query_time"


def test_q3_adds_freshness_window():
    sql = read("queries/Q3_time_sensitive_status.sql")
    assert "INTERVAL" in sql and "support_valid" in sql


def test_structured_state_view_excludes_news():
    sql = read("views/v_structured_state.sql")
    assert "state_type = 'C_S'" in sql
    assert "news_claims_eligible" not in sql


def test_augmented_state_view_keeps_exclusion_reasons():
    sql = read("views/v_augmented_state.sql")
    assert "state_type = 'C_SU'" in sql
    for column in (
        "news_claims_excluded_after_query_time",
        "news_claims_excluded_stale",
        "news_claims_excluded_unsupported",
        "news_claims_excluded_syndicated",
    ):
        assert column in sql


def test_b1_reads_cs_and_p1_reads_csu():
    assert "v_structured_state" in read("views/v_policy_b1.sql")
    assert "v_augmented_state" in read("views/v_policy_p1.sql")


def test_b0_ignores_conflict_state():
    sql = read("views/v_policy_b0.sql")
    assert "'D'" in sql
    assert "conflict_states" not in sql


def test_ddl_covers_every_layer_including_route_log():
    names = {p.name for p in (SQL / "ddl").glob("*.sql")}
    assert {
        "bronze_sources.sql",
        "silver_entities.sql",
        "silver_evidence_claims.sql",
        "gold_conflict_states.sql",
        "gold_query_workload.sql",
        "gold_gold_labels.sql",
        "gold_route_log.sql",
    } <= names
