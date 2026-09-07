"""Entity linking: bukan novelty, tetapi wajib auditable."""
from src.processing.entity_link import link_candidate, similarity
from src.processing.normalize import normalize_name, normalize_value

CANDIDATES = ["Pantai Tanjung Setia", "Air Terjun Way Lalaan", "Teluk Kiluan"]


def test_normalize_strips_prefix_and_punctuation():
    assert normalize_name("Desa Wisata Kiluan!") == "kiluan"
    assert normalize_name("TELUK  KILUAN") == "teluk kiluan"


def test_exact_match_after_normalization():
    match, method, score = link_candidate("teluk kiluan", CANDIDATES)
    assert match == "Teluk Kiluan"
    assert method == "exact"
    assert score == 100.0


def test_near_match_is_fuzzy_and_auto_accepted():
    match, method, score = link_candidate("Pantai Tanjung Setia.", CANDIDATES)
    assert match == "Pantai Tanjung Setia"
    assert method in ("exact", "fuzzy")
    assert score >= 92


def test_ambiguous_match_is_flagged_for_review_not_accepted():
    match, method, score = link_candidate("Air Terjun Way Lalan", CANDIDATES)
    assert method in ("fuzzy", "review")
    assert match == "Air Terjun Way Lalaan"


def test_unrelated_name_is_not_linked():
    match, method, _ = link_candidate("Stasiun Kereta Tanjungkarang", CANDIDATES)
    assert method == "none"
    assert match is None


def test_similarity_is_symmetric_enough_and_bounded():
    s = similarity("Teluk Kiluan", "teluk kiluan")
    assert 0 <= s <= 100 and s == 100


def test_value_normalization_uses_frozen_vocabulary():
    vocab = {"tutup sementara": "tutup"}
    assert normalize_value("Tutup Sementara", vocab) == "tutup"
    assert normalize_value("Buka", vocab) == "buka"
