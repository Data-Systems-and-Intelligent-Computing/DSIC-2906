"""Taksonomi kegagalan (minimal 20 kasus diaudit).

Pengelompokan penting: kegagalan sumber/ekstraksi tidak boleh terbaca sebagai
kegagalan routing, karena extraction bukan objek penelitian ini.
"""
FAILURE_CATEGORIES = [
    "entity_link_error",
    "extraction_error",
    "invalid_support_span",
    "source_dependence",
    "syndicated_story",
    "stale_news",
    "temporal_mismatch",
    "normalization_error",
    "taxonomy_mismatch",
    "missing_structured_value",
    "conflicting_fresh_reports",
    "ambiguous_gold",
    "conflict_state_error",
    "routing_error",
    "unnecessary_abstention",
    "unnecessary_verification",
    "unsupported_direct_answer",
    "obsolete_answer",
    "insufficient_evidence",
    "acquisition_failure",
]

FAILURE_GROUPS = {
    "source_data": [
        "source_dependence",
        "syndicated_story",
        "stale_news",
        "missing_structured_value",
        "acquisition_failure",
        "conflicting_fresh_reports",
    ],
    "extraction": [
        "entity_link_error",
        "extraction_error",
        "invalid_support_span",
        "normalization_error",
        "taxonomy_mismatch",
    ],
    "conflict_state": [
        "conflict_state_error",
        "temporal_mismatch",
        "insufficient_evidence",
        "ambiguous_gold",
    ],
    "routing": [
        "routing_error",
        "unnecessary_abstention",
        "unnecessary_verification",
        "unsupported_direct_answer",
        "obsolete_answer",
    ],
}

MIN_AUDITED_CASES = 20


def group_of(category):
    for group, members in FAILURE_GROUPS.items():
        if category in members:
            return group
    raise ValueError(f"Kategori tidak dikenal: {category}")


def summarize_cases(cases):
    """Ringkas kasus yang diaudit per kategori dan per kelompok."""
    by_category, by_group = {}, {}
    for case in cases:
        category = case["category"]
        by_category[category] = by_category.get(category, 0) + 1
        group = group_of(category)
        by_group[group] = by_group.get(group, 0) + 1
    return {
        "n_cases": len(cases),
        "meets_minimum": len(cases) >= MIN_AUDITED_CASES,
        "by_category": by_category,
        "by_group": by_group,
    }
