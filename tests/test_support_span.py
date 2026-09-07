"""Claim unstructured tanpa span pendukung tidak boleh jadi corroboration."""
from src.evidence.support_span import has_valid_support_span, mark_support_validity

SPAN = "Pengelola menyatakan lokasi wisata ini tutup sementara sejak pekan lalu."


def news(value, span_text):
    return {
        "representation_type": "unstructured_text",
        "normalized_value": value,
        "support_span": {"text": span_text} if span_text else None,
    }


def test_structured_claim_needs_no_span():
    assert has_valid_support_span({"representation_type": "structured", "normalized_value": "buka"})


def test_valid_span_accepted():
    assert has_valid_support_span(news("tutup", SPAN))


def test_missing_span_rejected():
    assert not has_valid_support_span(news("tutup", None))


def test_span_that_does_not_mention_value_is_rejected():
    # Span ada, tetapi tidak mendukung nilai yang diklaim.
    assert not has_valid_support_span(news("buka", SPAN))


def test_span_too_short_rejected():
    assert not has_valid_support_span(news("tutup", "tutup"))


def test_mark_support_validity_does_not_mutate_input():
    claims = [news("tutup", SPAN), news("buka", None)]
    marked = mark_support_validity(claims)
    assert [c["support_valid"] for c in marked] == [True, False]
    assert "support_valid" not in claims[0]
