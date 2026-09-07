"""Figure wajib (daftar lengkap ada di README).

Aturan yang harus dipatuhi setiap plot reliability: risk tidak pernah
digambar tanpa coverage pada figure yang sama.
"""
REQUIRED_FIGURES = [
    "architecture_lineage",
    "acquisition_corpus_table",
    "source_coverage_table",
    "extraction_audit_table",
    "entity_link_audit_table",
    "conflict_transition_cs_to_csu",
    "policy_comparison_b0_b1_b2_p1",
    "risk_coverage_plot",
    "dcr_bdcr_harmful_plot",
    "verification_abstention_plot",
    "latency_p50_p95_table",
    "evidence_touched_distribution",
    "time_sensitive_vs_stable_breakdown",
    "failure_taxonomy",
    "publication_boundary_table",
]


def risk_coverage_plot(summaries, out_path):
    raise NotImplementedError("Implementasikan pada H19-H21 (scripts/12_analyze_results.sh).")


def dcr_bdcr_plot(breakdowns, out_path):
    raise NotImplementedError("Implementasikan pada H19-H21 (scripts/12_analyze_results.sh).")
