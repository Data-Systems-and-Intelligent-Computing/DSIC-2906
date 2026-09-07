"""P1 Cross-Format Conflict-Aware Query Handler.

Inilah objek penelitian: keputusan query-time Direct / Verify / Abstain
berdasarkan conflict state yang sudah diperkaya berita temporally eligible.

    CLEAN        -> Direct
    MODERATE     -> Verify
    SEVERE       -> Abstain
    INSUFFICIENT -> Abstain

Verify yang tidak menemukan supported value berakhir Abstain, bukan menebak
(ditegakkan di src/routing/verification.py).
"""
POLICY = "P1"
STATE_TYPE = "C_SU"

RULE = {
    "CLEAN": "D",
    "MODERATE": "V",
    "SEVERE": "A",
    "INSUFFICIENT": "A",
}


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
