-- Coverage evidence per atribut: dasar keputusan H7 (pemilihan atribut final)
-- dan gate "minimal dua time-sensitive attributes punya coverage".
--
-- independent_sources dihitung dari kombinasi family+lineage, bukan dari
-- jumlah baris: syndication tidak menambah kemerdekaan sumber.
SELECT
  c.attribute,
  COUNT(*)                                   AS n_claims,
  COUNT(DISTINCT c.entity_id)                AS n_entities,
  COUNT(DISTINCT CASE WHEN c.source_family <> 'jadesta' THEN c.entity_id END) AS n_entities_with_external,
  COUNT(DISTINCT CASE WHEN c.representation_type = 'unstructured_text' THEN c.entity_id END) AS n_entities_with_news,
  COUNT(DISTINCT COALESCE(c.story_lineage_id, c.source_family)) AS independent_sources,
  SUM(CASE WHEN c.support_valid THEN 1 ELSE 0 END) AS n_supported_claims
FROM iceberg.silver.evidence_claims c
GROUP BY c.attribute
ORDER BY n_entities DESC;
