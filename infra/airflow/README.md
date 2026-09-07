# Airflow — Opsional

Airflow **tidak wajib**. README menetapkan: jika tidak stabil dalam 1–2 hari
pertama, pakai `scripts/` + `Makefile` dan lanjutkan penelitian.

Orkestrasi bukan kontribusi ilmiah DSIC-2906; ia hanya menjalankan urutan yang
sama dengan `scripts/`.

## Menjalankan (profil terpisah, tidak ikut `up` default)

```bash
docker compose --env-file .env --profile orchestration up -d airflow
# UI di http://localhost:8081
```

DAG: `dag_dsic2906.py`, memanggil script yang sama persis dengan jalur manual
sehingga kedua jalur menghasilkan hasil identik.

## Batas

DAG berhenti di `07_build_gold`. Tahap held-out freeze, eksperimen utama, dan
analisis sengaja dijalankan manual karena masing-masing punya gate yang harus
diperiksa manusia sebelum tahap berikutnya boleh berjalan.
