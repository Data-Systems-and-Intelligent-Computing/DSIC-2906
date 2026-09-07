-- B1 Structured-Only Conflict Handling.
-- Rule IDENTIK dengan P1; satu-satunya perbedaan adalah state (C_S vs C_SU).
-- Kesamaan rule inilah yang mengisolasi value-of-news.
CREATE OR REPLACE VIEW iceberg.gold.v_policy_b1 AS
SELECT
  w.request_id,
  w.entity_id,
  w.attribute,
  w.query_time,
  'B1' AS policy,
  'C_S' AS state_type,
  COALESCE(s.label, 'INSUFFICIENT') AS conflict_label,
  CASE COALESCE(s.label, 'INSUFFICIENT')
    WHEN 'CLEAN'    THEN 'D'
    WHEN 'MODERATE' THEN 'V'
    ELSE 'A'
  END AS action,
  CASE COALESCE(s.label, 'INSUFFICIENT') WHEN 'CLEAN' THEN true ELSE false END AS answered_if_direct,
  CASE COALESCE(s.label, 'INSUFFICIENT') WHEN 'MODERATE' THEN true ELSE false END AS verification_invoked
FROM iceberg.gold.query_workload w
LEFT JOIN iceberg.gold.v_structured_state s
  ON  s.entity_id  = w.entity_id
  AND s.attribute  = w.attribute
  AND s.query_time = w.query_time;
