# Arsitektur

## Aliran data

```text
JADESTA CSV | Wikidata | Wikipedia | Tourism News
        v
MinIO Raw Zone            snapshot immutable + manifest + checksum
        v
Spark                     parsing, normalisasi, linking, ekstraksi
        v
Iceberg Bronze            source-preserving + metadata akuisisi
        v
Iceberg Silver            canonical entities + evidence claims + provenance
        v
Iceberg Gold              C_S, C_SU, query workload, gold labels, route log
        v
Trino                     B0 | B1 | B2 | P1
        v
route log                 action, answered, evidence touched, latency
```

## Layer dan tanggung jawabnya

| Layer | Tanggung jawab | Yang TIDAK dilakukan |
|---|---|---|
| Raw | menyimpan payload apa adanya + provenance | tidak ada parsing |
| Bronze | bentuk sumber dipertahankan | tidak ada normalisasi |
| Silver | normalisasi, linking, claim, support span | tidak ada conflict state |
| Gold | C_S, C_SU, workload, gold, route log | tidak ada perubahan rule |

## Titik kontrol yang menentukan validitas

1. **Cutoff as-of query_time** — di `src/processing/temporal_filter.py` dan
   di setiap query SQL. Ini pertahanan utama terhadap temporal leakage.
2. **Support span** — di `src/evidence/support_span.py`. Claim tanpa span
   pendukung tidak menjadi corroboration.
3. **Story lineage** — di `src/evidence/corroboration.py`. Syndication tidak
   menambah kemerdekaan sumber.
4. **Isolasi C_S vs C_SU** — B1 dan P1 memakai tabel rule yang sama persis;
   satu-satunya perbedaan adalah state. Inilah yang membuat selisih keduanya
   terbaca sebagai value-of-news, bukan efek rule yang berbeda.

## Katalog

Spark dan Trino berbagi satu Iceberg REST catalog. Gate penelitian
mensyaratkan keempat policy membaca snapshot yang identik; katalog terpisah
membuat syarat itu tidak dapat dibuktikan.
