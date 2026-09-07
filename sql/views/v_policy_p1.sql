-- P1 Cross-Format Conflict-Aware Query Handler.
--   CLEAN -> Direct | MODERATE -> Verify | SEVERE/INSUFFICIENT -> Abstain
-- Verify yang tidak menemukan supported value berakhir Abstain (ditentukan
-- di src/routing/verification.py, bukan di view ini).
CREATE OR REPLACE VIEW iceberg.gold.v_policy_p1 AS
SELECT
  w.request_id,
  w.entity_id,
  w.attribute,
  w.query_time,
  'P1'  AS policy,
  'C_SU' AS state_type,
  COALESCE(a.label, 'INSUFFICIENT') AS conflict_label,
  CASE COALESCE(a.label, 'INSUFFICIENT')
    WHEN 'CLEAN'    THEN 'D'
    WHEN 'MODERATE' THEN 'V'
    ELSE 'A'
  END AS action,
  CASE COALESCE(a.label, 'INSUFFICIENT') WHEN 'MODERATE' THEN true ELSE false END AS verification_invoked
FROM iceberg.gold.query_workload w
LEFT JOIN iceberg.gold.v_augmented_state a
  ON  a.entity_id  = w.entity_id
  AND a.attribute  = w.attribute
  AND a.query_time = w.query_time;
