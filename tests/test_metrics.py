"""Metrik primer, value-of-news, dan cost."""
from src.evaluation.bootstrap import paired_bootstrap
from src.evaluation.metrics import (
    abstention_rate,
    answer_coverage,
    beneficial_decision_change_rate,
    change_breakdown,
    decision_change_rate,
    harmful_decision_change_rate,
    selective_accuracy,
    selective_risk,
    summarize,
    unsupported_answer_rate,
    verification_rate,
)


def r(rid, action, answered, correct=None, unsupported=False, entity=None, verify=False, value=None):
    return {
        "request_id": rid,
        "entity_id": entity or f"e{rid}",
        "action": action,
        "answered": answered,
        "correct": correct,
        "unsupported": unsupported,
        "verification_invoked": verify,
        "returned_value": value,
    }


RESULTS = [
    r("1", "D", True, correct=True, value="buka"),
    r("2", "D", True, correct=False, unsupported=True, value="buka"),
    r("3", "A", False),
    r("4", "V", True, correct=True, verify=True, value="tutup"),
]


def test_selective_metrics():
    assert selective_accuracy(RESULTS) == 2 / 3
    assert selective_risk(RESULTS) == 1 / 3
    assert answer_coverage(RESULTS) == 3 / 4
    assert unsupported_answer_rate(RESULTS) == 1 / 3


def test_cost_metrics():
    assert verification_rate(RESULTS) == 1 / 4
    assert abstention_rate(RESULTS) == 1 / 4


def test_abstain_everything_gives_no_risk_but_zero_coverage():
    # Justru inilah alasan risk tidak boleh dilaporkan sendirian.
    all_abstain = [r(str(i), "A", False) for i in range(5)]
    assert answer_coverage(all_abstain) == 0.0
    assert selective_risk(all_abstain) is None


def test_empty_input_returns_none_not_crash():
    assert selective_accuracy([]) is None
    assert answer_coverage([]) is None


def test_summary_always_reports_risk_with_coverage():
    s = summarize(RESULTS)
    assert s["selective_risk"] is not None
    assert s["answer_coverage"] is not None
    assert s["verification_rate"] is not None


BASELINE = [
    r("1", "D", True, correct=False, unsupported=True, value="buka"),  # jawaban buruk
    r("2", "D", True, correct=True, value="buka"),                     # jawaban baik
    r("3", "D", True, correct=True, value="buka"),                     # tidak berubah
]
TREATMENT = [
    r("1", "V", True, correct=True, verify=True, value="tutup"),       # diperbaiki
    r("2", "A", False),                                                # dirusak
    r("3", "D", True, correct=True, value="buka"),                     # tetap
]


def test_decision_change_rate():
    assert decision_change_rate(BASELINE, TREATMENT) == 2 / 3


def test_beneficial_and_harmful_changes_are_separated():
    counts = change_breakdown(BASELINE, TREATMENT)
    assert counts["changed"] == 2
    assert counts["beneficial"] == 1
    assert counts["harmful"] == 1
    assert beneficial_decision_change_rate(BASELINE, TREATMENT) == 0.5
    assert harmful_decision_change_rate(BASELINE, TREATMENT) == 0.5


def test_no_change_gives_none_not_zero_division():
    assert beneficial_decision_change_rate(BASELINE, BASELINE) is None


def test_paired_bootstrap_resamples_entities():
    base = [r(str(i), "D", True, correct=False, entity=f"e{i % 5}") for i in range(20)]
    treat = [r(str(i), "D", True, correct=True, entity=f"e{i % 5}") for i in range(20)]
    out = paired_bootstrap(base, treat, selective_accuracy, iterations=200, seed=1)
    assert out["n_entities"] == 5
    assert out["point"] == 1.0
    assert out["ci_low"] <= out["point"] <= out["ci_high"]
