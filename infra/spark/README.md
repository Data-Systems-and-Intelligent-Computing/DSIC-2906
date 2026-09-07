# Spark / PySpark — Batch Processing

Spark menangani Raw→Bronze→Silver→Gold: parsing, normalisasi, persiapan
entity linking, temporal filtering, materialisasi evidence claim, dan
pembentukan conflict state.

Spark **bukan** query engine eksperimen; B0/B1/B2/P1 dijalankan di Trino.

## Katalog bersama

Konfigurasi ada di `infra/iceberg/catalog.properties`. Spark dan Trino wajib
menunjuk REST catalog dan warehouse yang sama — gate penelitian mensyaratkan
keempat policy membaca snapshot Iceberg yang identik.

## Menjalankan

```bash
docker compose --env-file .env exec spark \
  spark-submit --properties-file infra/iceberg/catalog.properties \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.1,org.apache.iceberg:iceberg-aws-bundle:1.9.1 \
  <job.py>
```

Versi Spark, Iceberg runtime, dan AWS bundle dibekukan di
`configs/environment.yaml` dan disalin ke `docs/reproducibility.md`.

## Urutan yang tidak boleh dibalik

Gold dibangun **setelah** conflict rule, freshness window, dan routing rule
dibekukan. Membangun ulang Gold dengan rule berbeda setelah held-out dibuka
adalah routing leakage.
