-- Gold: workload beku. Identik untuk B0/B1/B2/P1 (gate penelitian).
CREATE TABLE IF NOT EXISTS iceberg.gold.query_workload (
  request_id         VARCHAR,
  entity_id          VARCHAR,
  attribute          VARCHAR,
  query_time         TIMESTAMP(6) WITH TIME ZONE,
  query_type         VARCHAR,   -- Q1 | Q2 | Q3
  profile_id         VARCHAR,
  attribute_class    VARCHAR,   -- time_sensitive | stable_control
  in_heldout         BOOLEAN,
  has_news_evidence  BOOLEAN    -- stratum sampling; BUKAN input routing
)
WITH (format = 'PARQUET');
