-- C_S: conflict state dari structured evidence saja (dasar B1).
-- Hanya claim structured; berita sengaja tidak disertakan.
CREATE OR REPLACE VIEW iceberg.gold.v_structured_state AS
SELECT
  entity_id,
  attribute,
  query_time,
  label,
  eligible_claim_count,
  distinct_normalized_values,
  independent_source_count,
  corroborated_value,
  rule_version
FROM iceberg.gold.conflict_states
WHERE state_type = 'C_S';
