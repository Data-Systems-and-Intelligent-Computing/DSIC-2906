"""B2 Always Verify: upper-cost comparator."""
from src.routing import policy_b2


def test_always_verify_regardless_of_state():
    for label in ("CLEAN", "MODERATE", "SEVERE", "INSUFFICIENT"):
        d = policy_b2.decide({}, {"label": label})
        assert d["action"] == "V"
        assert d["verification_invoked"] is True


def test_uses_augmented_state():
    assert policy_b2.STATE_TYPE == "C_SU"
