"""B1 Structured-Only Conflict Handling."""
from src.routing import policy_b1, policy_p1


def test_reads_structured_only_state():
    assert policy_b1.STATE_TYPE == "C_S"


def test_rule_table_is_identical_to_p1():
    # Ini yang mengisolasi value-of-news: rule sama, state berbeda.
    for label in ("CLEAN", "MODERATE", "SEVERE", "INSUFFICIENT"):
        assert policy_b1.decide({}, {"label": label})["action"] == \
               policy_p1.decide({}, {"label": label})["action"]


def test_missing_state_abstains():
    assert policy_b1.decide({}, None)["action"] == "A"
