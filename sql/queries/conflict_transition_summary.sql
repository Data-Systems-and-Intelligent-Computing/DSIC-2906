-- Transisi C_S -> C_SU: berapa sering penambahan berita mengubah conflict state.
-- Mengisi figure/tabel wajib no. 6 dan menjadi dasar pembacaan DCR.
SELECT
  s.label AS structured_label,
  a.label AS augmented_label,
  COUNT(*) AS n_requests,
  COUNT(DISTINCT s.entity_id) AS n_entities
FROM iceberg.gold.v_structured_state s
JOIN iceberg.gold.v_augmented_state a
  ON  a.entity_id  = s.entity_id
  AND a.attribute  = s.attribute
  AND a.query_time = s.query_time
GROUP BY s.label, a.label
ORDER BY n_requests DESC;
