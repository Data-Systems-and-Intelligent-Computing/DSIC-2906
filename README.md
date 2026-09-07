# DSIC-2906 — Conflict-Aware Query Handling across Structured Records and Unstructured Tourism Evidence

Repository penelitian untuk topik **DSIC-2906**.

Judul Indonesia yang direkomendasikan:

> **Direct, Verify, atau Abstain? Penanganan Query Berbasis Konflik pada Rekaman Terstruktur dan Evidence Berita Pariwisata**

Judul artikel bahasa Inggris yang direkomendasikan:

> **Direct, Verify, or Abstain? Conflict-Aware Query Handling across Structured Records and Unstructured Tourism Evidence**

Alternatif judul yang lebih systems-oriented:

> **Cross-Format Conflict-Aware Query Handling: Reliability–Coverage Trade-offs with Structured Records and News Evidence**

---

## Keputusan Pembimbing

Penelitian dapat dikerjakan dalam satu bulan, tetapi dengan asumsi bahwa **data belum siap sebagai evidence store**.

JADESTA baru tersedia sebagai raw scraped CSV. Wikidata/Wikipedia dan corpus berita wisata perlu diakuisisi, dinormalisasi, ditautkan ke entity yang sama, dan dimaterialisasi sebagai auditable evidence claims sebelum eksperimen utama dapat berjalan.

Karena itu, Minggu 1 harus mencakup:

- acquisition;
- raw snapshots;
- manifests dan checksums;
- candidate pool;
- entity linking;
- claim extraction;
- minimum viable lakehouse;
- source cutoff;
- freeze schema dan rule.

Namun seluruh pekerjaan upstream tersebut hanyalah **enabling infrastructure**.

Novelty artikel bukan:

- scraping;
- crawler;
- MinIO;
- Iceberg;
- Spark;
- Trino;
- Airflow;
- entity linking;
- information extraction;
- LLM extraction;
- learned confidence;
- evidence fusion;
- Policy Gate;
- RAG;
- physical query optimizer.

Kontribusi ilmiah tetap:

> **query-time conflict handling yang memutuskan kapan sebuah value dikembalikan langsung, kapan perlu diverifikasi menggunakan evidence lintas format, dan kapan sistem harus abstain.**

---

## Kalimat Jangkar Penelitian

> Penelitian ini menguji apakah penambahan temporally anchored unstructured news evidence ke structured records dapat membentuk conflict state yang lebih informatif untuk keputusan query-time Direct, Verify, atau Abstain, sehingga selective answer reliability meningkat tanpa collapse pada answer coverage atau verification cost yang berlebihan.

---

## Publication Boundary

DSIC-2906 memiliki boundary berikut:

> **DSIC-2906 owns the query-time decision of WHEN to return a structured value directly, WHEN to consult fixed structured/unstructured evidence, and WHEN to abstain.**

DSIC-2906 tidak mengklaim kontribusi pada:

- evidence extraction;
- truth discovery;
- learned source reliability;
- evidence fusion;
- confidence calibration;
- Policy Gate design;
- retrieval ranking;
- RAG;
- hallucination evaluation;
- join order;
- access path;
- physical query plan.

---

## Posisi Penelitian

Objek ilmiah:

```text
query-time conflict handling
```

Unit keputusan:

```text
entity × attribute × query time
```

Action:

```text
D = Direct
V = Verify
A = Abstain
```

Main policies:

```text
B0 Uniform Direct
B1 Structured-Only Conflict Handling
B2 Always Verify
P1 Cross-Format Conflict-Aware Query Handler
```

---

## Research Question

### RQ Utama

**RQ1. Does conflict-aware query handling over structured records and temporally anchored unstructured evidence improve selective answer reliability compared with uniform direct execution and structured-only conflict handling, while maintaining acceptable answer coverage and verification cost?**

### Sub-RQ

**RQ2.** Seberapa sering penambahan unstructured news evidence mengubah conflict state atau keputusan Direct/Verify/Abstain dibanding structured-only handling?

**RQ3.** Dari keputusan yang berubah, berapa proporsi yang beneficial karena mencegah incorrect, unsupported, atau obsolete answer, dan berapa yang harmful atau tidak perlu?

**RQ4.** Apakah P1 mengurangi selective risk dan unsupported-answer rate dibanding B0 dan B1 tanpa collapse pada answer coverage?

**RQ5.** Berapa verification work dan latency P1 dibanding B2 Always Verify pada query trace yang sama?

**RQ6 — Sekunder.** Apakah manfaat unstructured evidence lebih besar pada atribut time-sensitive dibanding atribut yang relatif stabil?

RQ1–RQ5 adalah core article.

RQ6 hanya dilakukan bila coverage cukup.

---

## Hipotesis

### H1 — Incremental Reliability

P1 diharapkan mempunyai selective risk dan unsupported-answer rate lebih rendah daripada B1 pada coverage yang masih substantif.

Jika tidak, hasil tetap valid: news mungkin tidak menambah information value atau extraction/temporal noise terlalu besar.

### H2 — Beneficial Decision Change

Diharapkan:

```text
BDCR > Harmful Decision Change Rate
```

pada requests yang berubah setelah news ditambahkan.

### H3 — Coverage Preservation

Reliability gain tidak boleh diperoleh hanya dengan:

```text
abstain hampir seluruh request
```

### H4 — Verification Efficiency

P1 diharapkan memakai verification lebih sedikit daripada B2 Always Verify dengan reliability yang tidak memburuk secara material.

### H5 — Temporal Usefulness

Manfaat news diperkirakan lebih tinggi pada atribut yang time-sensitive dibanding stable-control attribute.

Semua hipotesis boleh ditolak.

---

## Data Sources

### S1 — JADESTA

Peran:

```text
structured seed
```

Input awal:

```text
raw scraped CSV
```

Aturan:

- ingest seluruh CSV;
- simpan checksum;
- simpan scraping provenance;
- jangan menganggap JADESTA sebagai ground truth.

### S2 — Wikidata

Peran:

```text
structured corroboration
```

Acquisition:

```text
SPARQL / API
```

### S3 — Wikipedia

Peran:

```text
unstructured / semi-structured textual evidence
```

Acquisition:

```text
MediaWiki API / export
```

Wikidata dan Wikipedia diberi family lineage:

```text
Wikimedia
```

agar tidak dihitung sebagai dua independent sources secara naif.

### U1…Un — Tourism News

Peran:

```text
temporally anchored unstructured evidence
```

Acquisition:

- targeted requests;
- Scrapy;
- BeautifulSoup;
- Trafilatura.

Simpan:

- URL;
- publisher;
- publication timestamp;
- fetched timestamp;
- HTTP status;
- discovery query/seed;
- checksum;
- raw text/HTML;
- origin/story lineage.

---

## Source Dependence dan Syndication

Jumlah halaman bukan jumlah bukti independen.

Contoh:

```text
1 press release
   ↓
repost A
repost B
repost C
```

bukan:

```text
3 independent corroborations
```

Gunakan story/origin lineage.

---

## Candidate Pool

Full JADESTA di-ingest.

External enrichment dibatasi pada:

```text
300–500 entities
```

Candidate pool harus dibekukan sebelum external enrichment selesai.

Pemilihan dapat berbasis stratification yang transparan, misalnya:

- region;
- category;
- source coverage;
- availability.

Jangan memilih entity berdasarkan hasil P1.

---

## Attribute Scope

Target:

```text
2 time-sensitive attributes
+
1 stable-control attribute
```

Kandidat time-sensitive:

- operational/access status;
- facility/accessibility condition;
- safety/advisory/temporary condition.

Stable control:

- category;
- location descriptor.

Final attributes dibekukan setelah coverage audit di akhir Minggu 1.

---

## Held-Out Gold

Target:

```text
100–150 entities
×
3 attributes
≈
300–450 entity–attribute–time requests
```

Sampling harus mencakup:

- with news;
- without news;
- clean agreement;
- structured conflict;
- augmented conflict;
- time-sensitive cases;
- stable-control cases bila tersedia.

Gold set tidak boleh hanya berisi known conflicts.

---

## Gold Standard

Gold unit:

```text
entity_id
attribute
query_time
```

Gold outcome:

- accepted value(s);
- unresolved/unknown;
- not-applicable.

Gold dinilai **as-of query time**.

Evidence setelah query time dilarang.

Berita bukan otomatis ground truth.

Majority source bukan otomatis benar.

---

## Annotation Protocol

Sebelum held-out test:

- freeze entity list;
- freeze query time;
- freeze source cutoff;
- freeze evidence cutoff.

Setiap request harus dapat ditelusuri ke:

- structured value;
- article/reference;
- normalized claim;
- source lineage;
- URL;
- published_at/observed_at;
- fetched_at;
- supporting span.

Second annotation:

- 20–25% gold requests;
- minimal 20% news claims atau sekitar 100 claims jika feasible.

Disagreement harus diadjudicate sebelum final evaluation.

---

## Evidence Claim Schema

Common representation:

```text
claim = (
  entity_id,
  attribute,
  source_lineage,
  representation_type,
  normalized_value,
  published_or_observed_at,
  support_span
)
```

Recommended additional fields:

- source_id;
- source_family;
- story_lineage;
- fetched_at;
- URL/reference;
- extractor_version;
- temporal eligibility.

Main study tidak memakai learned source weights.

---

## Supporting Span

Setiap unstructured claim wajib memiliki:

```text
support_span
```

Jika span tidak benar-benar mendukung normalized value:

```text
unsupported claim
```

Claim tersebut tidak boleh menjadi corroboration.

---

## Conflict State

### Structured-Only

```text
C_S(e,a)
```

menggunakan structured evidence saja.

### Augmented

```text
C_SU(e,a,tq)
```

menggunakan structured + temporally eligible news claims.

Eligible news harus memenuhi:

- publication/observation time valid;
- tidak melampaui query time;
- freshness window;
- support span valid;
- story lineage tidak duplikatif.

---

## Conflict Labels

### CLEAN

Eligible claims setuju setelah normalization dan temporal filtering.

### MODERATE

Ada perbedaan, tetapi ada corroborated value atau evidence baru yang perlu verification.

### SEVERE

Important claims bertentangan tanpa dasar cukup untuk memilih supported value dengan fixed verification rule.

### INSUFFICIENT

Evidence relevan tidak cukup.

---

## Freshness Window

Time-sensitive attributes memakai freshness rule yang dibekukan sebelum held-out test.

Jangan:

- menggunakan artikel setelah query time;
- mengubah window setelah melihat hasil;
- menganggap artikel lama selalu masih valid.

---

## Policy B0 — Uniform Direct

Selalu mengembalikan structured seed/canonical value.

News dan conflict state tidak memengaruhi decision.

Peran:

```text
baseline: semua query diperlakukan sama
```

---

## Policy B1 — Structured-Only Conflict Handling

Conflict state dibentuk dari structured evidence saja.

Gunakan rule Direct/Verify/Abstain yang sama sejauh mungkin.

Tujuan:

```text
mengisolasi value structured conflict awareness
```

---

## Policy B2 — Always Verify

Semua requests:

- membaca eligible structured claims;
- membaca eligible news claims;
- menjalankan fixed verification routine.

Peran:

```text
upper-cost comparator
```

---

## Policy P1 — Cross-Format Conflict-Aware Query Handler

State:

```text
structured + eligible news
```

Rule:

```text
CLEAN        → Direct
MODERATE     → Verify
SEVERE       → Abstain
INSUFFICIENT → Abstain
```

Jika Verify tidak mendapatkan supported value:

```text
Abstain
```

---

## Verification Routine

Verification bukan novelty.

Routine tetap:

1. baca eligible claims;
2. cek provenance;
3. cek temporal validity;
4. cek support span;
5. cek fixed corroboration rule;
6. return supported value atau abstain.

Rule dibekukan sebelum held-out.

---

## Query Workload

### Q1 — Entity–Attribute Point Lookup

Wajib.

```sql
SELECT requested_attribute
FROM entity_view
WHERE entity_id = ?
-- evaluated as-of query_time
```

Unit analisis utama:

```text
entity × attribute × query time
```

### Q2 — Multi-Attribute Entity Profile

Wajib sekunder.

Meminta 2–3 attributes untuk satu entity.

Routing dievaluasi per cell.

Whole-profile correctness secondary.

### Q3 — Time-Sensitive Status Query

Opsional artikel.

Contoh:

```text
apakah destinasi dapat diakses/beroperasi pada query time tertentu?
```

Q3 tidak boleh berubah menjadi RAG/QA benchmark.

---

## Arsitektur Minimum

```text
JADESTA CSV
+
Wikidata API/SPARQL
+
Wikipedia API/export
+
Tourism News Crawler
        ↓
MinIO Raw Zone
immutable snapshots
manifest + checksum
        ↓
Spark Batch Processing
        ↓
Iceberg Bronze
source-preserving records
        ↓
Iceberg Silver
canonical entities
evidence claims
temporal fields
provenance
story lineage
        ↓
Iceberg Gold
C_S
C_SU
query workload
gold labels
        ↓
Trino
        ↓
B0 | B1 | B2 | P1
        ↓
route log
evidence touched
latency
risk / coverage
DCR / BDCR
```

---

## Peran Tools

### Python

- crawler;
- API acquisition;
- extractor;
- routing controller;
- annotation export/import;
- analysis.

### MinIO

Raw zone untuk:

- CSV;
- JSON;
- HTML;
- text;
- source payload;
- manifests;
- checksums.

### Apache Iceberg

Bronze/Silver/Gold untuk:

- versioned tables;
- snapshots;
- replay;
- consistent schema.

### Spark / PySpark

Batch:

- parsing;
- normalization;
- entity-link preparation;
- temporal filtering;
- evidence-claim materialization;
- conflict-state generation.

### Trino

Menjalankan:

- B0;
- B1;
- B2;
- P1;
- Q1/Q2/Q3;
- evidence lookup;
- latency measurement.

### Airflow

Opsional.

Jika tidak stabil dalam 1–2 hari pertama, gunakan scripts/Makefile.

---

## Minimum Viable Lakehouse

Wajib:

```text
Raw
Bronze
Silver
Gold
```

Tidak perlu:

- Kafka;
- Flink;
- Kubernetes;
- vector database;
- RAG;
- agent.

---

## E0 — Acquisition & Lakehouse Sanity

1. deploy stack;
2. ingest JADESTA;
3. freeze candidate pool;
4. acquire Wikidata/Wikipedia;
5. acquire targeted news;
6. create source manifests;
7. checksum raw payloads;
8. record publication/fetched time;
9. story-lineage grouping;
10. build Bronze/Silver;
11. pilot 30–50 entities;
12. freeze source cutoff.

Gate:

- snapshots reproducible;
- entity links auditable;
- claims have support spans;
- source cutoff frozen;
- at least two time-sensitive attributes have sufficient coverage.

---

## E1 — Normalization, Linking, Extraction Audit

Lakukan:

- normalization;
- entity linking;
- fixed extraction;
- support-span extraction;
- manual audit.

Entity linking boleh:

- rule based;
- fuzzy;
- manual review.

Jangan diklaim novelty.

Audit minimal:

```text
100 claims atau ~20%
```

---

## E2 — Conflict-State Augmentation

Pada request yang sama, hitung:

```text
C_S
vs
C_SU
```

Catat transition:

```text
CLEAN → MODERATE
CLEAN → SEVERE
MODERATE → CLEAN
INSUFFICIENT → MODERATE
...
```

Freeze held-out setelah development rules final.

---

## E3 — Main Policy Comparison

Jalankan:

```text
B0
B1
B2
P1
```

pada Q1 held-out workload.

Hitung:

- selective accuracy;
- selective risk;
- coverage;
- unsupported answer rate;
- DCR;
- BDCR;
- harmful change;
- verification rate;
- abstention rate.

---

## E4 — Value-of-News Ablation

Main comparison:

```text
B1 vs P1
```

Classify changed decisions:

- beneficial;
- harmful;
- neutral/unnecessary.

Analisis:

- apakah news mencegah unsupported answer?
- apakah news memulihkan supported answer?
- apakah news hanya membuat abstention?
- apakah benefit terkonsentrasi pada time-sensitive attributes?

---

## E5 — Cost, Latency, Robustness

Gunakan frozen snapshots dan fixed query trace.

Latency protocol:

- warm-up;
- randomized policy order;
- 10–20 measured repetitions;
- p50/median;
- p95.

Catat:

- evidence claims touched;
- articles touched;
- route;
- query ID;
- latency;
- resource context.

Crawling latency tidak masuk query-time latency.

---

## E6 — Failure Analysis

Audit minimal 20 cases.

Kategori:

1. entity-link error;
2. extraction error;
3. invalid support span;
4. source dependence;
5. syndicated story;
6. stale news;
7. temporal mismatch;
8. normalization error;
9. taxonomy mismatch;
10. missing structured value;
11. conflicting fresh reports;
12. ambiguous gold;
13. conflict-state error;
14. routing error;
15. unnecessary abstention;
16. unnecessary verification;
17. unsupported direct answer;
18. obsolete answer;
19. insufficient evidence;
20. acquisition failure.

Pisahkan:

- source/data failure;
- extraction failure;
- conflict-state failure;
- routing failure.

---

## Primary Metrics

### Selective Accuracy

```text
correct answered requests / answered requests
```

### Selective Risk

```text
incorrect answered requests / answered requests
```

### Answer Coverage

```text
answered requests / all requests
```

### Unsupported Answer Rate

```text
unsupported answered requests / answered requests
```

---

## Value-of-News Metrics

### DCR

Decision Change Rate:

```text
changed route/output requests / all requests
```

### BDCR

Beneficial Decision Change Rate:

proporsi changed decisions yang:

- mencegah incorrect answer;
- mencegah unsupported answer;
- mencegah obsolete answer;
- memulihkan supported answer.

### Harmful Decision Change Rate

Changed decisions yang:

- membuat supported answer menjadi salah;
- menyebabkan unnecessary abstain;
- menyebabkan unnecessary verify;
- menghilangkan useful answer.

### News Evidence Utilization Rate

Proporsi requests di mana eligible news benar-benar dipakai oleh fixed verification routine.

---

## Cost Metrics

- Verification Rate;
- Abstention Rate;
- p50 latency;
- p95 latency;
- evidence claims touched;
- articles touched.

---

## Risk–Coverage Principle

Accuracy tidak boleh dilaporkan sendirian.

Sistem yang:

```text
abstain 100%
```

bisa punya risk rendah tetapi coverage nol.

Karena itu selalu laporkan:

```text
risk + coverage + verification
```

---

## Analisis Statistik

Gunakan paired design.

Request/entity yang sama diuji pada B0/B1/B2/P1.

### Bootstrap

Gunakan paired bootstrap 95% CI dengan resampling pada:

```text
entity level
```

bukan article atau claim row.

### McNemar

Opsional untuk matched correct/incorrect decisions.

### Latency

- warm-up;
- randomized policy order;
- 10–20 repetitions;
- median;
- p95.

### Freeze Before Held-Out

- analysis plan;
- freshness window;
- extractor;
- entity-link rule;
- normalization;
- conflict rule;
- routing rule.

---

## Scientific Completion

Penelitian selesai walaupun P1 tidak mengungguli B1.

P1 hanya dapat disebut lebih praktis jika hasil mendukung:

- risk turun;
- unsupported answer turun;
- coverage tidak collapse;
- BDCR > harmful change;
- verification lebih rendah dari B2;
- reliability tidak turun material.

Jika news merugikan, laporkan sebagai hasil.

---

## Threats to Validity

### Source Dependence

Gunakan story lineage.

### Gold Uncertainty

Gold boleh unresolved.

### Temporal Leakage

Evidence setelah query time dilarang.

### Stale Evidence

Gunakan fixed freshness window.

### Extraction Error

Pisahkan dari routing error.

### Entity Linking Error

Audit terpisah.

### Coverage Bias

Entity populer lebih sering diberitakan.

### Routing Leakage

Jangan ubah rule setelah held-out.

### Overlap dengan Penelitian Lain

Jangan mengklaim:

- fusion;
- confidence calibration;
- Policy Gate;
- RAG;
- retrieval;
- hallucination.

### Systems Generalization

Lakehouse stack adalah testbed, bukan otomatis novelty “big data”.

---

## Quality Gate — Minggu 1

- [ ] MinIO berjalan reproducibly.
- [ ] Iceberg snapshot dapat dibaca.
- [ ] Spark dan Trino melihat data yang konsisten.
- [ ] JADESTA raw di-ingest.
- [ ] Candidate pool 300–500 dibekukan.
- [ ] Wikidata/Wikipedia acquired.
- [ ] Tourism news acquired.
- [ ] Source manifest tersedia.
- [ ] Checksums tersedia.
- [ ] Publication/fetched timestamps tersedia.
- [ ] Story lineage tersedia.
- [ ] Claim schema tersedia.
- [ ] Entity linking auditable.
- [ ] Support span tersedia.
- [ ] Minimal dua time-sensitive attributes punya coverage.
- [ ] Source cutoff frozen.

Jika gate gagal:

- kecilkan candidate pool;
- kecilkan publisher count;
- jangan menambah arsitektur.

---

## Quality Gate — Minggu 2

- [ ] Bronze selesai.
- [ ] Silver selesai.
- [ ] Gold selesai.
- [ ] C_S tersedia.
- [ ] C_SU tersedia.
- [ ] Query workload tersedia.
- [ ] Route-log schema tersedia.
- [ ] Gold subset dipilih.
- [ ] 300–450 requests atau alasan eksplisit bila lebih kecil.
- [ ] 20–25% second annotation.
- [ ] 100/20% claim audit.
- [ ] Held-out entities frozen.
- [ ] Held-out articles frozen.
- [ ] Query times frozen.
- [ ] Extractor frozen.
- [ ] Entity-link rule frozen.
- [ ] Conflict rule frozen.
- [ ] Routing rule frozen.

---

## Quality Gate — Penelitian

- [ ] Raw→Bronze→Silver→Gold replayable.
- [ ] Source snapshots frozen.
- [ ] Checksums frozen.
- [ ] Every news claim has entity_id.
- [ ] Every news claim has story lineage.
- [ ] Every news claim has published_at.
- [ ] Every news claim has support span.
- [ ] Syndication not counted as independent corroboration.
- [ ] B0/B1/B2/P1 use identical snapshots.
- [ ] Same query workload.
- [ ] Same gold set.
- [ ] Same Trino configuration.
- [ ] Same hardware/resource cap.
- [ ] Accuracy reported with coverage.
- [ ] DCR reported with BDCR/harmful change.
- [ ] B2 Always Verify available.
- [ ] Route logs saved.
- [ ] Evidence touched saved.
- [ ] Bootstrap unit = entity.
- [ ] 20 failure cases audited.
- [ ] No upstream novelty overclaim.

---

## Quality Gate — Artikel

- [ ] Semua quality gate penelitian selesai.
- [ ] Final literature search 2021–2026 selesai.
- [ ] Direct prior art checked.
- [ ] Novelty statement updated if needed.
- [ ] Acquisition provenance documented.
- [ ] Gold annotation reproducible.
- [ ] News claim audit reproducible.
- [ ] Main claims held-out.
- [ ] Temporal cutoff obeyed.
- [ ] Risk–coverage–verification complete.
- [ ] Beneficial/harmful change complete.
- [ ] Artifact reproduces one main table.
- [ ] Artifact reproduces one main figure.
- [ ] Coverage bias discussed.
- [ ] Syndication discussed.
- [ ] Temporal mismatch discussed.
- [ ] Extraction error discussed.
- [ ] No “first” claim without evidence.

---

## Rencana Kerja 1 Bulan

### Minggu 1 (Hari 1–7) — Acquisition dan Minimum Viable Lakehouse

Hari 1–2:

- freeze RQ;
- freeze publication boundary;
- deploy MinIO/Iceberg/Spark/Trino;
- Airflow hanya bila stabil;
- ingest JADESTA.

Hari 3–4:

- candidate pool;
- Wikidata;
- Wikipedia;
- targeted news;
- manifests;
- checksums;
- source timestamps;
- story lineage.

Hari 5–6:

- Raw→Bronze;
- Bronze→Silver;
- normalization;
- entity linking;
- claim extraction;
- support-span audit.

Hari 7:

- pilot 30–50 entities;
- coverage audit;
- choose final attributes;
- freeze source cutoff;
- freeze methodological rules.

### Minggu 2 (Hari 8–14) — Evidence Tables, Gold, Held-Out Freeze

Hari 8–10:

- canonical entity;
- evidence claim;
- C_S;
- C_SU;
- query workload;
- route schema.

Hari 11–12:

- gold subset;
- annotation;
- second review;
- extraction audit.

Hari 13–14:

- adjudication;
- freeze held-out;
- freeze query times;
- final sanity.

### Minggu 3 (Hari 15–21) — Main Experiment

Hari 15–18:

- B0/B1/B2/P1 on Q1;
- risk;
- coverage;
- unsupported rate;
- DCR;
- BDCR;
- harmful change.

Hari 19–21:

- repeated latency benchmark;
- Q2 if stable;
- bootstrap CI;
- failure analysis;
- results v1 freeze.

### Minggu 4 (Hari 22–30) — Reproduction dan Artikel

Hari 22–24:

- fresh clean-environment rerun;
- reproduce one main table;
- reproduce one main figure.

Hari 25–26:

- final literature verification;
- failure taxonomy;
- threats to validity.

Hari 27–28:

- Methods;
- Results;
- Discussion;
- publication boundary.

Hari 29–30:

- manuscript v0.8–v1.0;
- artifact freeze;
- supervisor review;
- presentation material.

---

## Grafik dan Tabel Wajib

1. Architecture/data-lineage diagram.
2. Acquisition/corpus table.
3. Source coverage table.
4. Extraction audit table.
5. Entity-link audit table.
6. Conflict-state transition C_S → C_SU.
7. B0/B1/B2/P1 policy comparison.
8. Risk–coverage plot.
9. DCR/BDCR/harmful change plot.
10. Verification/abstention plot.
11. p50/p95 latency table.
12. Evidence-touched distribution.
13. Time-sensitive vs stable-control breakdown.
14. Failure taxonomy.
15. Publication-boundary table.

---

## Struktur Repository

```text
dsic-2906/
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
├── Makefile
├── docker-compose.yml            # MinIO + mc init + Iceberg REST + Trino + Spark (+Airflow opsional)
├── configs/
│   ├── sources.yaml              # sumber + family lineage (wikimedia)
│   ├── acquisition.yaml          # etika crawling + field provenance wajib
│   ├── entity_linking.yaml       # threshold accept/review; bukan novelty
│   ├── claim_extraction.yaml     # ekstraktor beku + aturan support span
│   ├── conflict_rules.yaml       # CLEAN/MODERATE/SEVERE/INSUFFICIENT
│   ├── freshness.yaml            # window per atribut + aturan anti-leakage
│   ├── routing.yaml              # tabel rule B0/B1/B2/P1
│   ├── experiment.yaml           # pool, held-out, metrik, latency, statistik
│   ├── annotation.yaml           # protokol gold + second annotation
│   └── environment.yaml          # cap resource + image ter-pin
├── infra/
│   ├── trino/catalog/iceberg.properties   # katalog REST (bukan hadoop)
│   ├── iceberg/catalog.properties         # katalog Spark, harus sama dgn Trino
│   ├── minio/README.md
│   ├── spark/README.md
│   └── airflow/
│       ├── README.md
│       └── dag_dsic2906.py       # opsional; berhenti di build_gold
├── data/
│   ├── README.md
│   ├── raw/{jadesta,wikidata,wikipedia,news}/
│   ├── bronze/  silver/  gold/
│   ├── checksums/
│   ├── manifests/
│   │   ├── source_manifest.csv
│   │   ├── candidate_pool.csv
│   │   ├── entity_manifest.csv
│   │   ├── news_manifest.csv
│   │   ├── story_lineage.csv
│   │   ├── claim_manifest.csv
│   │   ├── query_workload.csv
│   │   └── source_cutoff.yaml
│   └── annotations/
│       ├── gold_requests.csv
│       ├── news_claim_audit.csv
│       ├── entity_link_audit.csv
│       └── adjudication_log.csv
├── schemas/                      # 8 kontrak JSON Schema
│   ├── source_snapshot.schema.json
│   ├── canonical_entity.schema.json
│   ├── evidence_claim.schema.json
│   ├── conflict_state.schema.json
│   ├── query_request.schema.json
│   ├── route_log.schema.json
│   ├── gold_label.schema.json
│   └── raw_result.schema.json
├── sql/
│   ├── ddl/                      # bronze_sources, silver_*, gold_* (termasuk route_log)
│   ├── views/                    # v_structured_state, v_augmented_state, v_policy_{b0,b1,b2,p1}
│   └── queries/                  # Q1, Q2, Q3, conflict_transition_summary, coverage_summary
├── src/
│   ├── acquisition/              # ingest_jadesta, fetch_wikidata, fetch_wikipedia,
│   │                             # crawl_news, source_manifest, story_lineage
│   ├── processing/               # normalize, entity_link, temporal_filter,
│   │                             # materialize_{bronze,silver,gold}
│   ├── evidence/                 # claim_extractor, support_span, corroboration, conflict_state
│   ├── routing/                  # policy_{b0,b1,b2,p1}, verification, route_logger
│   ├── annotation/               # export_gold_form, import_gold, agreement, adjudicate
│   ├── evaluation/               # metrics, bootstrap, latency_benchmark,
│   │                             # failure_analysis, run_workload, plots
│   └── utils/                    # config, hashing, logging, time
├── tests/                        # 13 file, 75 test
├── scripts/                      # 00-13, satu langkah pipeline per script
├── results/
│   ├── README.md                 # schema route log + aturan pelaporan
│   ├── raw/ processed/ figures/ tables/ failure_cases/
├── docs/
│   ├── architecture.md
│   ├── publication-boundary.md
│   ├── annotation-protocol.md
│   ├── failure-taxonomy.md
│   └── reproducibility.md
└── paper/
    ├── manuscript.md
    └── references.bib
```

Direktori yang terisi saat berjalan dan diabaikan Git: `data/raw/**`,
`data/{bronze,silver,gold}/**`, `results/{raw,processed}/**`, `volumes/`.

---

## Setup Minimum

```bash
cp .env.example .env       # isi MINIO_ROOT_PASSWORD dan identitas crawler
make setup                 # venv + dependencies
make up                    # MinIO + Iceberg REST + Trino + Spark
make test                  # 75 unit test
make ps
```

Airflow tidak ikut `up` default:

```bash
docker compose --env-file .env --profile orchestration up -d airflow
```

Katalog Iceberg memakai tipe `rest`, bukan `hadoop`: Trino tidak mendukung
katalog Iceberg berbasis filesystem, dan Spark (writer) serta Trino (reader)
wajib melihat snapshot yang sama persis.

### Urutan pipeline

```bash
make ingest      # 01        JADESTA -> raw zone
make acquire     # 02-03     Wikidata/Wikipedia + berita tertarget
make freeze      # 04        bekukan source cutoff (akhir Minggu 1)
make bronze      # 05        Raw -> Bronze
make silver      # 06        Bronze -> Silver + coverage audit
make gold        # 07        Silver -> Gold (setelah rule dibekukan)
make annotate    # 08        ekspor formulir gold
make heldout     # 09        bekukan held-out + checksum rule
make experiment  # 10        B0/B1/B2/P1 pada Q1
make latency     # 11        benchmark latency query-time
make analyze     # 12        metrik, bootstrap, figure, failure analysis
make reproduce   # 13        rerun dari environment bersih
```

---

## Catatan Pembimbing

Alur besarnya kira-kira seperti ini:

```text
JADESTA CSV
+
Wikidata
+
Wikipedia
+
Tourism News
        ↓
source acquisition
URL / ID
published_at
fetched_at
checksum
story lineage
        ↓
MinIO Raw
        ↓
Spark
        ↓
Iceberg Bronze
        ↓
normalization
entity linking
claim extraction
support span
        ↓
Iceberg Silver
canonical entities
evidence claims
temporal provenance
        ↓
structured-only state C_S
        ↓
add eligible news
        ↓
augmented state C_SU
        ↓
Gold workload
entity × attribute × query time
        ↓
B0 | B1 | B2 | P1
        ↓
Direct | Verify | Abstain
        ↓
risk
coverage
unsupported answers
DCR
BDCR
harmful changes
verification work
latency
        ↓
paired entity-level bootstrap
        ↓
failure analysis
        ↓
answer:
WHEN should the system return,
verify, or abstain?
```

Secara eksperimen dapat dipahami seperti berikut.

1. **Mulai dari JADESTA raw CSV, bukan dari asumsi bahwa evidence store sudah tersedia.** Ingest seluruh JADESTA ke raw zone. Simpan checksum dan provenance. Jangan langsung menganggap value JADESTA sebagai truth.

2. **Pilih candidate pool 300–500 entitas.** External enrichment hanya untuk pool ini agar pekerjaan satu bulan tetap realistis.

3. **Acquire Wikidata dan Wikipedia.** Wikidata menjadi structured corroboration. Wikipedia menjadi textual evidence. Beri keduanya family lineage Wikimedia.

4. **Acquire targeted tourism news.** Jangan crawling seluruh web. Publisher dan candidate entity harus sudah dibekukan. Catat URL, publication time, fetched time, checksum, status, dan story lineage.

5. **Freeze source cutoff akhir Minggu 1.** Setelah cutoff tidak boleh ada source/publisher baru masuk held-out evaluation.

6. **Materialize Bronze.** Bronze mempertahankan bentuk sumber dan acquisition metadata.

7. **Bangun canonical entities.** Entity linking boleh rule-based, fuzzy, dan manual review pada ambiguous case. Ini bukan novelty.

8. **Ekstrak evidence claims.** Structured dan unstructured harus berakhir pada common claim schema.

9. **Support span wajib.** News claim tanpa span yang mendukung normalized value tidak boleh menjadi corroboration.

10. **Audit extraction dan linking.** Minimal sekitar 100 claims atau 20% sample. Pisahkan extraction error dari routing error.

11. **Bangun C_S.** Ini conflict state yang hanya memakai structured evidence.

12. **Bangun C_SU.** Tambahkan news yang eligible berdasarkan temporal cutoff, freshness, support, dan story lineage.

13. **Freeze conflict rules.** CLEAN, MODERATE, SEVERE, INSUFFICIENT harus punya definisi tetap.

14. **Bangun gold subset.** Target 100–150 entities × 3 attributes, sekitar 300–450 requests, dengan query-time labels.

15. **Lakukan second annotation.** Review 20–25% gold requests dan audit news claims. Adjudicate disagreement sebelum final test.

16. **Jalankan B0.** Semua query Direct menggunakan structured seed. Ini baseline paling sederhana.

17. **Jalankan B1.** Structured-only conflict handling. Comparator ini penting untuk mengetahui apakah news benar-benar menambah value.

18. **Jalankan B2.** Always Verify menggunakan semua eligible structured + news claims. Ini upper-cost comparator.

19. **Jalankan P1.** CLEAN→Direct, MODERATE→Verify, SEVERE/INSUFFICIENT→Abstain.

20. **Gunakan paired request comparison.** B0/B1/B2/P1 harus memakai request, snapshot, gold, hardware, dan query workload yang sama.

21. **Risk harus dibaca bersama coverage.** Reliability tidak boleh “menang” hanya karena sistem abstain berlebihan.

22. **DCR mengukur seberapa sering news benar-benar mengubah decision.** Kalau DCR sangat kecil, incremental value news mungkin juga kecil.

23. **BDCR dan harmful changes adalah inti value-of-news.** Perubahan baru berguna jika mencegah wrong/unsupported/obsolete answer lebih sering daripada membuat keputusan memburuk.

24. **B2 menunjukkan verification upper cost.** Jika P1 mendekati Always Verify pada semua request, routing tidak memberi penghematan.

25. **Latency hanya query-time pada frozen snapshots.** Crawling dan preprocessing latency tidak masuk.

26. **Failure analysis minimal 20 cases.** Pisahkan source, extraction, temporal, conflict-state, dan routing failures.

27. **Hasil negatif tetap valid.** Jika news menyebabkan lebih banyak harmful abstention atau verification, itu tetap temuan yang sah.

28. **Jangan menambah RAG.** Penelitian berhenti pada supported value / abstain, bukan natural-language answer generation.

29. **Jangan mengklaim truth discovery.** Verification routine hanya memutuskan apakah supported value cukup tersedia.

30. **Jangan mengklaim scraping sebagai novelty.** Scraping hanya substrate.

31. **Hasil akhir harus menjawab pertanyaan berikut:** kapan structured value cukup aman untuk dikembalikan langsung, kapan evidence lintas format perlu diverifikasi, dan kapan sistem sebaiknya abstain?

Untuk tools, stack minimum adalah **MinIO + Apache Iceberg + Spark + Trino**. Python dipakai untuk acquisition, extraction, routing controller, annotation, bootstrap, dan plotting. Airflow opsional bila stabil. Tidak perlu Kafka, Flink, Kubernetes, vector DB, RAG, atau agent untuk menjawab RQ.

Yang paling penting: penelitian DSIC-2906 bukan **“bagaimana menggabungkan structured dan unstructured data?”**, tetapi **“apakah temporally anchored unstructured evidence memberi incremental conflict signal yang cukup berguna untuk memperbaiki keputusan Direct/Verify/Abstain dibanding structured-only handling, tanpa membayar coverage dan verification cost terlalu besar?”**
