"""B2 Always Verify.

Setiap request menjalankan verification routine, apa pun conflict label-nya.
Perannya adalah upper-cost comparator: jika P1 mendekati B2 pada semua
request, routing tidak memberi penghematan.
"""
POLICY = "B2"
STATE_TYPE = "C_SU"


def decide(request=None, state=None):
    return {
        "policy": POLICY,
        "state_type": STATE_TYPE,
        "conflict_label": (state or {}).get("label", "INSUFFICIENT"),
        "action": "V",
        "verification_invoked": True,
    }
