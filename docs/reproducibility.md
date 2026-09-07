# Reproducibility

## Cara menjalankan ulang

```bash
cp .env.example .env          # isi MINIO_ROOT_PASSWORD dan identitas crawler
make setup                    # venv + dependencies
make up                       # MinIO + Iceberg REST + Trino + Spark
make test                     # 75 unit test
bash scripts/13_reproduce_main.sh
```

## Versi yang harus dibekukan

Isi tabel ini sebelum eksperimen utama; salin nilainya dari
`docker compose images` dan `configs/environment.yaml`.

| Komponen | Versi |
|---|---|
| OS / kernel | FILL |
| Docker | FILL |
| Python | FILL |
| MinIO | FILL |
| Iceberg REST | FILL |
| Trino | FILL |
| Spark | FILL |
| Iceberg runtime | FILL |
| Airflow (bila dipakai) | FILL |

## Artefak yang dibekukan

| Artefak | Lokasi | Dibekukan pada |
|---|---|---|
| Source snapshot + checksum | `data/manifests/`, `data/checksums/` | akhir Minggu 1 |
| Source & evidence cutoff | `data/manifests/source_cutoff.yaml` | akhir Minggu 1 |
| Rule (conflict, freshness, routing, linking, extraction) | `configs/*.yaml` | sebelum held-out |
| Query workload | `data/manifests/query_workload.csv` | sebelum held-out |
| Gold labels | `data/annotations/gold_requests.csv` | setelah adjudikasi |
| Checksum freeze held-out | `data/checksums/heldout_freeze.sha256` | `scripts/09_freeze_heldout.sh` |

## Syarat perbandingan yang sah

B0/B1/B2/P1 wajib memakai snapshot Iceberg, query workload, gold set,
konfigurasi Trino, dan resource cap yang **sama**. Route log menyimpan
`snapshot_id` agar syarat ini dapat diperiksa setelah fakta, bukan sekadar
diasumsikan.

## Yang tidak masuk pengukuran latency

Crawling dan preprocessing. Yang diukur hanya biaya keputusan query-time di
atas frozen snapshot.

## Seed

`RANDOM_SEED=42` (`.env`), dipakai untuk sampling candidate pool, urutan
policy pada benchmark latency, dan bootstrap.
