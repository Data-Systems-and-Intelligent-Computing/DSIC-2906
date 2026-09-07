"""Menjalankan query workload untuk keempat policy.

Gate penelitian: B0/B1/B2/P1 wajib memakai snapshot, workload, gold set,
konfigurasi Trino, dan resource cap yang sama.
"""
from src.routing import POLICIES
from src.routing.route_logger import write_route
from src.routing.verification import resolve_action, verify
from src.utils.logging import get_logger

log = get_logger(__name__)


def run_request(request, claims, states, policy_name, freshness_window_days=None):
    """Jalankan satu request pada satu policy dan kembalikan baris route log."""
    policy = POLICIES[policy_name]
    state = states.get(policy.STATE_TYPE)
    decision = policy.decide(request, state)

    result = None
    if decision["action"] in ("D", "V"):
        result = verify(claims, request["query_time"], freshness_window_days)

    action, value, answered = resolve_action(decision["action"], result)

    return {
        "request_id": request["request_id"],
        "entity_id": request["entity_id"],
        "attribute": request["attribute"],
        "query_time": request["query_time"],
        "policy": decision["policy"],
        "state_type": decision["state_type"],
        "conflict_label": decision["conflict_label"],
        "action": action,
        "answered": answered,
        "returned_value": value,
        "verification_invoked": decision["verification_invoked"],
        "evidence_claims_touched": (result or {}).get("evidence_claims_touched", 0),
        "articles_touched": (result or {}).get("articles_touched", 0),
        "latency_ms": 0.0,
        "warmup": False,
    }


def run_all(requests, claims_by_request, states_by_request, path=None):
    raise NotImplementedError(
        "Sambungkan ke Trino dan tulis route log pada H15-H18 "
        "(scripts/10_run_main_experiment.sh)."
    )
