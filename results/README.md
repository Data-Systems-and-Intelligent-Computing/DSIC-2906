# Results

| Direktori | Isi | Masuk Git? |
|---|---|---|
| `raw/` | route log dan latency JSONL apa adanya | tidak |
| `processed/` | metrik teragregasi, bootstrap CI | tidak |
| `figures/` | figure wajib | ya, saat freeze |
| `tables/` | tabel manuskrip | ya, saat freeze |
| `failure_cases/` | ≥20 kasus yang diaudit | ya |

## Route log (`raw/route_log.jsonl`)

Satu baris per (request, policy, repetition); schema di
`schemas/route_log.schema.json`. Field yang menentukan hasil:

| Field | Kegunaan |
|---|---|
| `action` | D / V / A — dasar coverage dan abstention rate |
| `answered` | false untuk Abstain dan Verify yang gagal menemukan supported value |
| `value_supported` | dasar unsupported answer rate |
| `verification_invoked` | dasar verification rate dan perbandingan biaya vs B2 |
| `evidence_claims_touched`, `articles_touched` | biaya evidence |
| `snapshot_id` | bukti keempat policy memakai snapshot yang sama |

## Aturan pelaporan

Risk tidak pernah dilaporkan tanpa coverage dan verification. Sistem yang
abstain 100% memiliki risk nol dan coverage nol; angka risk sendirian tidak
bermakna.

DCR selalu dilaporkan bersama BDCR dan harmful change rate — mengetahui bahwa
berita mengubah keputusan tidak sama dengan mengetahui perubahannya membantu.
