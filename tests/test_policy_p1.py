"""P1 Cross-Format Conflict-Aware Query Handler."""
from src.routing import policy_p1
from src.routing.verification import resolve_action

CASES = {"CLEAN": "D", "MODERATE": "V", "SEVERE": "A", "INSUFFICIENT": "A"}


def test_routing_table():
    for label, expected in CASES.items():
        assert policy_p1.decide({}, {"label": label})["action"] == expected


def test_uses_augmented_state():
    assert policy_p1.STATE_TYPE == "C_SU"


def test_verification_only_on_moderate():
    assert policy_p1.decide({}, {"label": "MODERATE"})["verification_invoked"]
    assert not policy_p1.decide({}, {"label": "CLEAN"})["verification_invoked"]


def test_verify_without_supported_value_becomes_abstain():
    action, value, answered = resolve_action("V", {"value": None})
    assert (action, value, answered) == ("A", None, False)


def test_verify_with_supported_value_answers():
    action, value, answered = resolve_action("V", {"value": "tutup"})
    assert (action, value, answered) == ("V", "tutup", True)


def test_abstain_never_answers():
    assert resolve_action("A", {"value": "tutup"}) == ("A", None, False)
