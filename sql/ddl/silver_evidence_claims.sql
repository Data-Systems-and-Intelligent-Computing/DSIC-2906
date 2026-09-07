-- Silver: representasi bersama untuk evidence structured dan unstructured.
--
-- Dua kolom yang menentukan kebenaran hasil:
--   support_valid     -> claim unstructured tanpa span pendukung tidak boleh
--                        menjadi corroboration;
--   story_lineage_id  -> syndication dari satu origin dihitung SATU, bukan N.
CREATE TABLE IF NOT EXISTS iceberg.silver.evidence_claims (
  claim_id                  VARCHAR,
  entity_id                 VARCHAR,
  attribute                 VARCHAR,
  raw_value                 VARCHAR,
  normalized_value          VARCHAR,
  source_id                 VARCHAR,
  source_family             VARCHAR,   -- wikimedia menyatukan wikidata+wikipedia
  story_lineage_id          VARCHAR,
  representation_type       VARCHAR,
  published_or_observed_at  TIMESTAMP(6) WITH TIME ZONE,
  fetched_at                TIMESTAMP(6) WITH TIME ZONE,
  url_or_reference          VARCHAR,
  snapshot_id               VARCHAR,
  support_span_text         VARCHAR,
  support_span_start        INTEGER,
  support_span_end          INTEGER,
  support_valid             BOOLEAN,
  extractor_version         VARCHAR
)
WITH (format = 'PARQUET');
