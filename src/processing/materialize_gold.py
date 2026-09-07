"""Silver -> Gold: C_S, C_SU, query workload, gold labels.

Gold dibangun SETELAH rule conflict/freshness/routing dibekukan. Membangun
ulang Gold dengan rule berbeda setelah held-out membuka pintu routing leakage.
"""
from src.evidence.conflict_state import build_state
from src.utils.logging import get_logger

log = get_logger(__name__)


def build_conflict_states(claims_by_request, freshness_window_days=None):
    """Bangun pasangan C_S dan C_SU untuk setiap request.

    Keduanya dihitung dari kumpulan claim yang sama persis, sehingga selisih
    label sepenuhnya berasal dari penambahan berita.
    """
    rows = []
    for (entity_id, attribute, query_time), claims in claims_by_request.items():
        for state_type in ("C_S", "C_SU"):
            state = build_state(claims, query_time, state_type, freshness_window_days)
            state.update({"entity_id": entity_id, "attribute": attribute})
            rows.append(state)
    return rows


def materialize(rows, table):
    raise NotImplementedError("Implementasikan dengan Spark pada H8-H10 (scripts/07_build_gold.sh).")
