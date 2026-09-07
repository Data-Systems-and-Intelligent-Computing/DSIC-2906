"""Syndication: satu origin di-repost N kali tetap satu suara."""
from src.acquisition.story_lineage import assign_lineage, group_sizes, lineage_key
from src.evidence.corroboration import corroborated_values, count_independent_sources

TITLE = "Pantai X Ditutup Sementara"
PARA = "Pengelola menutup kawasan wisata sejak Senin."


def test_same_story_gets_same_lineage_key():
    assert lineage_key(TITLE, PARA) == lineage_key(TITLE, PARA)


def test_canonical_url_takes_priority():
    a = lineage_key("judul berbeda", "isi berbeda", canonical_url="https://asal/berita/1")
    b = lineage_key(TITLE, PARA, canonical_url="https://asal/berita/1")
    assert a == b


def test_reposts_collapse_into_one_group():
    articles = [
        {"title": TITLE, "first_paragraph": PARA, "publisher": "A"},
        {"title": TITLE, "first_paragraph": PARA, "publisher": "B"},
        {"title": TITLE, "first_paragraph": PARA, "publisher": "C"},
    ]
    assigned = assign_lineage(articles)
    assert len(set(group_sizes(assigned))) == 1
    assert max(group_sizes(assigned).values()) == 3


def test_syndicated_reposts_are_not_three_corroborations():
    claims = [
        {"normalized_value": "tutup", "source_family": f"pub{i}", "story_lineage_id": "L1"}
        for i in range(3)
    ]
    assert count_independent_sources(claims) == 1
    # Satu suara tidak memenuhi ambang dua sumber independen.
    assert corroborated_values(claims, min_independent_sources=2) == set()


def test_wikidata_and_wikipedia_count_as_one_family():
    claims = [
        {"normalized_value": "buka", "source_id": "wikidata", "source_family": "wikimedia"},
        {"normalized_value": "buka", "source_id": "wikipedia", "source_family": "wikimedia"},
    ]
    assert count_independent_sources(claims) == 1
