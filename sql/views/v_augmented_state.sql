-- C_SU: structured + news yang temporally eligible (dasar B2 dan P1).
-- Kolom excluded_* dipertahankan agar value-of-news dapat dijelaskan.
CREATE OR REPLACE VIEW iceberg.gold.v_augmented_state AS
SELECT
  entity_id,
  attribute,
  query_time,
  label,
  eligible_claim_count,
  distinct_normalized_values,
  independent_source_count,
  corroborated_value,
  news_claims_eligible,
  news_claims_excluded_after_query_time,
  news_claims_excluded_stale,
  news_claims_excluded_unsupported,
  news_claims_excluded_syndicated,
  rule_version
FROM iceberg.gold.conflict_states
WHERE state_type = 'C_SU';
