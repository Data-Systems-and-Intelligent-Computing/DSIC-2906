-- Q2: multi-attribute entity profile (2-3 atribut untuk satu entitas).
-- Routing dievaluasi PER SEL (entity x attribute), bukan per profil.
-- Whole-profile correctness bersifat sekunder.
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
  AND c.attribute IN (?, ?, ?)
  AND c.published_or_observed_at <= ?   -- query_time
ORDER BY c.attribute, c.published_or_observed_at DESC;
