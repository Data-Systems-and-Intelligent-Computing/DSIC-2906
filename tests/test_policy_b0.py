"""B0 Uniform Direct."""
from src.routing import policy_b0


def test_always_direct_regardless_of_state():
    for label in ("CLEAN", "MODERATE", "SEVERE", "INSUFFICIENT"):
        d = policy_b0.decide({}, {"label": label})
        assert d["action"] == "D"
        assert d["verification_invoked"] is False


def test_ignores_conflict_state_entirely():
    assert policy_b0.decide({}, None)["conflict_label"] == "NA"
    assert policy_b0.STATE_TYPE == "none"
