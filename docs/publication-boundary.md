# Publication Boundary

Dokumen ini adalah rujukan tetap saat menulis klaim. Setiap kalimat kontribusi
di manuskrip harus lolos tabel ini.

## Yang dimiliki DSIC-2906

> **Keputusan query-time tentang KAPAN sebuah structured value dikembalikan
> langsung, KAPAN evidence lintas format perlu dikonsultasikan, dan KAPAN
> sistem harus abstain.**

## Yang TIDAK diklaim

| Bukan kontribusi | Statusnya di sini |
|---|---|
| Evidence extraction | rule-based, dibekukan, diaudit; substrate |
| Truth discovery | verification hanya memutuskan ketersediaan supported value |
| Learned source reliability | tidak dipakai; tidak ada bobot sumber terlatih |
| Evidence fusion | tidak dilakukan |
| Confidence calibration | tidak dilakukan |
| Policy Gate design | tidak diklaim |
| Retrieval ranking / RAG | tidak dipakai; keluaran bukan bahasa alami |
| Hallucination evaluation | di luar cakupan |
| Entity linking | rule-based + fuzzy + manual; diaudit terpisah |
| Scraping / crawler | substrate akuisisi |
| MinIO / Iceberg / Spark / Trino / Airflow | testbed, bukan novelty |
| Join order / access path / physical plan | di luar cakupan |

## Uji kalimat

Sebelum menulis klaim, tanyakan: apakah kalimat ini tetap benar bila
extraction, linking, dan lakehouse diganti komponen lain yang setara?

- Ya → klaim berada di dalam boundary.
- Tidak → klaim itu milik pekerjaan upstream, bukan DSIC-2906.

## Larangan kata

Jangan memakai "first", "novel framework", "optimal", atau "state-of-the-art"
tanpa bukti langsung dari hasil. Jangan menyebut lakehouse stack sebagai
kontribusi "big data".
