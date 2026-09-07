-- B0 Uniform Direct: selalu kembalikan structured seed value.
-- Conflict state tidak memengaruhi keputusan. Ini baseline paling sederhana.
CREATE OR REPLACE VIEW iceberg.gold.v_policy_b0 AS
SELECT
  w.request_id,
  w.entity_id,
  w.attribute,
  w.query_time,
  'B0'  AS policy,
  'none' AS state_type,
  'NA'  AS conflict_label,
  'D'   AS action,
  true  AS answered,
  false AS verification_invoked
FROM iceberg.gold.query_workload w;
