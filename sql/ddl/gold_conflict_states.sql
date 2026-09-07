-- Gold: C_S dan C_SU untuk setiap entity x attribute x query_time.
-- Kolom excluded_* menjelaskan MENGAPA sebuah news claim tidak dipakai;
-- tanpa itu, analisis value-of-news tidak dapat memisahkan "news tidak ada"
-- dari "news ada tetapi tidak eligible".
CREATE TABLE IF NOT EXISTS iceberg.gold.conflict_states (
  entity_id                          VARCHAR,
  attribute                          VARCHAR,
  query_time                         TIMESTAMP(6) WITH TIME ZONE,
  state_type                         VARCHAR,   -- C_S | C_SU
  label                              VARCHAR,   -- CLEAN | MODERATE | SEVERE | INSUFFICIENT
  eligible_claim_count               INTEGER,
  distinct_normalized_values         INTEGER,
  independent_source_count           INTEGER,
  corroborated_value                 VARCHAR,
  news_claims_eligible               INTEGER,
  news_claims_excluded_after_query_time INTEGER,
  news_claims_excluded_stale         INTEGER,
  news_claims_excluded_unsupported   INTEGER,
  news_claims_excluded_syndicated    INTEGER,
  rule_version                       VARCHAR
)
WITH (format = 'PARQUET');
