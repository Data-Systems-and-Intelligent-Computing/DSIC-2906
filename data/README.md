# Data

## Zona

| Direktori | Isi | Masuk Git? |
|---|---|---|
| `raw/` | payload mentah immutable (JADESTA, Wikidata, Wikipedia, news) | tidak |
| `bronze/` | source-preserving + metadata akuisisi | tidak |
| `silver/` | canonical entities + evidence claims | tidak |
| `gold/` | C_S, C_SU, query workload, gold labels | tidak |
| `checksums/` | checksum snapshot dan freeze | ya |
| `manifests/` | manifest sumber, pool, entity, news, lineage, claim, workload | ya |
| `annotations/` | gold requests dan hasil audit | ya |

Yang di-commit hanya manifest, checksum, dan anotasi — bukan payload.

## Manifest

| File | Isi |
|---|---|
| `source_manifest.csv` | satu baris per snapshot mentah + checksum |
| `candidate_pool.csv` | 300–500 entitas, dibekukan sebelum enrichment eksternal |
| `entity_manifest.csv` | canonical entity + metode dan skor linking |
| `news_manifest.csv` | artikel + publisher + `published_at` + `fetched_at` |
| `story_lineage.csv` | pengelompokan syndication |
| `claim_manifest.csv` | evidence claim + support span + validitasnya |
| `query_workload.csv` | request beku (entity × attribute × query_time) |
| `source_cutoff.yaml` | cutoff sumber dan evidence |

## Anotasi

| File | Isi |
|---|---|
| `gold_requests.csv` | label gold, dinilai as-of query_time |
| `news_claim_audit.csv` | audit ekstraksi (≥100 claim atau ~20%) |
| `entity_link_audit.csv` | audit linking, terpisah dari routing |
| `adjudication_log.csv` | penyelesaian disagreement |

## Aturan yang mengikat

1. Raw zone immutable; akuisisi ulang menghasilkan snapshot baru.
2. Artikel tanpa `published_at` tidak akan pernah temporally eligible —
   catat saat akuisisi.
3. Setelah `source_cutoff.yaml` dibekukan, tidak ada sumber atau publisher
   baru yang boleh masuk evaluasi held-out.
4. JADESTA adalah structured seed, **bukan** ground truth.
