-- Q1: entity-attribute point lookup. Unit analisis utama.
-- Dievaluasi as-of query_time: klausa published_or_observed_at <= query_time
-- adalah aturan keras anti temporal leakage dan tidak boleh dihapus.
SELECT
  c.entity_id,
  c.attribute,
  c.normalized_value,
  c.source_id,
  c.source_family,
  c.story_lineage_id,
  c.published_or_observed_at,
  c.support_valid
FROM iceberg.silver.evidence_claims c
WHERE c.entity_id = ?
  AND c.attribute = ?
  AND c.published_or_observed_at <= ?   -- query_time
ORDER BY c.published_or_observed_at DESC;
