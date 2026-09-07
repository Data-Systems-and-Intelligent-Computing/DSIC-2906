-- Gold: route log, satu baris per (request, policy, repetition).
-- Gate penelitian mensyaratkan route log dan evidence-touched tersimpan.
CREATE TABLE IF NOT EXISTS iceberg.gold.route_log (
  request_id              VARCHAR,
  entity_id               VARCHAR,
  attribute               VARCHAR,
  query_time              TIMESTAMP(6) WITH TIME ZONE,
  policy                  VARCHAR,   -- B0 | B1 | B2 | P1
  state_type              VARCHAR,   -- none | C_S | C_SU
  conflict_label          VARCHAR,
  action                  VARCHAR,   -- D | V | A
  answered                BOOLEAN,
  returned_value          VARCHAR,
  value_supported         BOOLEAN,
  verification_invoked    BOOLEAN,
  evidence_claims_touched INTEGER,
  articles_touched        INTEGER,
  latency_ms              DOUBLE,
  repetition              INTEGER,
  warmup                  BOOLEAN,
  snapshot_id             VARCHAR,   -- wajib sama untuk keempat policy
  rule_version            VARCHAR
)
WITH (format = 'PARQUET');
