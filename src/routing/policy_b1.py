"""B1 Structured-Only Conflict Handling.

Memakai tabel rule yang IDENTIK dengan P1; satu-satunya perbedaan adalah
state yang dibaca (C_S, bukan C_SU). Kesamaan rule inilah yang membuat
selisih B1 vs P1 dapat dibaca sebagai value-of-news, bukan efek rule berbeda.
"""
from src.routing.policy_p1 import RULE

POLICY = "B1"
STATE_TYPE = "C_S"


def decide(request=None, state=None):
    label = (state or {}).get("label", "INSUFFICIENT")
    action = RULE.get(label, "A")
    return {
        "policy": POLICY,
        "state_type": STATE_TYPE,
        "conflict_label": label,
        "action": action,
        "verification_invoked": action == "V",
    }
