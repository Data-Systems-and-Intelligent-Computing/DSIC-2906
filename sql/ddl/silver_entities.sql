-- Silver: canonical entities hasil entity linking.
-- link_method dan link_score disimpan agar linking dapat diaudit terpisah
-- dari routing error (threats to validity).
CREATE TABLE IF NOT EXISTS iceberg.silver.entities (
  entity_id          VARCHAR,
  canonical_name     VARCHAR,
  normalized_key     VARCHAR,
  seed_source_id     VARCHAR,
  jadesta_id         VARCHAR,
  wikidata_qid       VARCHAR,
  wikipedia_title    VARCHAR,
  region             VARCHAR,
  category           VARCHAR,
  link_method        VARCHAR,   -- exact | fuzzy | manual | unlinked
  link_score         DOUBLE,
  link_reviewed_by   VARCHAR,
  in_candidate_pool  BOOLEAN,
  in_heldout         BOOLEAN
)
WITH (format = 'PARQUET');
