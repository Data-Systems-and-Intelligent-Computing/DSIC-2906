-- Gold: label anotasi, dinilai as-of query_time.
-- accepted_values berupa array karena beberapa nilai dapat sama-sama diterima.
CREATE TABLE IF NOT EXISTS iceberg.gold.gold_labels (
  request_id           VARCHAR,
  entity_id            VARCHAR,
  attribute            VARCHAR,
  query_time           TIMESTAMP(6) WITH TIME ZONE,
  outcome              VARCHAR,   -- accepted_value | unresolved_unknown | not_applicable
  accepted_values      ARRAY(VARCHAR),
  evidence_refs        ARRAY(VARCHAR),
  annotator_id         VARCHAR,
  annotated_at         TIMESTAMP(6) WITH TIME ZONE,
  is_second_annotation BOOLEAN,
  adjudicated          BOOLEAN,
  adjudication_note    VARCHAR
)
WITH (format = 'PARQUET');
