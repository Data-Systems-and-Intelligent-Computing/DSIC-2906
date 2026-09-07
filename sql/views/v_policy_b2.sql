-- B2 Always Verify: upper-cost comparator.
-- Setiap request menjalankan verification routine, apa pun conflict label-nya.
CREATE OR REPLACE VIEW iceberg.gold.v_policy_b2 AS
SELECT
  w.request_id,
  w.entity_id,
  w.attribute,
  w.query_time,
  'B2'  AS policy,
  'C_SU' AS state_type,
  COALESCE(a.label, 'INSUFFICIENT') AS conflict_label,
  'V'   AS action,
  true  AS verification_invoked
FROM iceberg.gold.query_workload w
LEFT JOIN iceberg.gold.v_augmented_state a
  ON  a.entity_id  = w.entity_id
  AND a.attribute  = w.attribute
  AND a.query_time = w.query_time;
