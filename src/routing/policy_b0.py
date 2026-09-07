"""B0 Uniform Direct.

Selalu mengembalikan structured seed value. Conflict state tidak memengaruhi
keputusan. Baseline paling sederhana: semua query diperlakukan sama.
"""
POLICY = "B0"
STATE_TYPE = "none"


def decide(request=None, state=None):
    """Selalu Direct, apa pun conflict state-nya."""
    return {
        "policy": POLICY,
        "state_type": STATE_TYPE,
        "conflict_label": "NA",
        "action": "D",
        "verification_invoked": False,
    }
