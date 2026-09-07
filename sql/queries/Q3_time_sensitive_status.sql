-- Q3: time-sensitive status query (opsional artikel).
-- Menambahkan freshness window di atas cutoff query_time.
--
-- Q3 TIDAK boleh berubah menjadi benchmark RAG/QA: keluarannya tetap
-- supported value atau abstain, bukan jawaban bahasa alami.
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
  AND c.published_or_observed_at <= ?                        -- query_time
  AND c.published_or_observed_at >= ? - INTERVAL '180' DAY   -- freshness window
  AND c.support_valid = true
ORDER BY c.published_or_observed_at DESC;
