-- Bronze: source-preserving. Bentuk sumber dan metadata akuisisi dipertahankan
-- apa adanya; normalisasi TIDAK dilakukan di layer ini.
CREATE TABLE IF NOT EXISTS iceberg.bronze.sources (
  snapshot_id           VARCHAR,
  source_id             VARCHAR,
  source_family         VARCHAR,
  representation_type   VARCHAR,   -- structured | semi_structured_text | unstructured_text
  url_or_reference      VARCHAR,
  publisher             VARCHAR,
  published_at          TIMESTAMP(6) WITH TIME ZONE,
  fetched_at            TIMESTAMP(6) WITH TIME ZONE,
  http_status           INTEGER,
  discovery_query       VARCHAR,
  story_lineage_id      VARCHAR,
  checksum_sha256       VARCHAR,
  raw_path              VARCHAR,
  content_type          VARCHAR,
  raw_payload           VARCHAR
)
WITH (format = 'PARQUET');
