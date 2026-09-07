# Taksonomi Kegagalan

Minimal 20 kasus diaudit (E6). Kategori didefinisikan di
`src/evaluation/failure_analysis.py`.

## Mengapa dikelompokkan

Extraction dan entity linking **bukan** objek penelitian ini. Jika kegagalan
ekstraksi terbaca sebagai kegagalan routing, kesimpulan tentang P1 menjadi
salah. Karena itu setiap kasus wajib masuk salah satu kelompok berikut.

## Kelompok

### 1. Source / data
`source_dependence`, `syndicated_story`, `stale_news`,
`missing_structured_value`, `acquisition_failure`, `conflicting_fresh_reports`

Kegagalan karena sifat sumber, bukan karena keputusan sistem.

### 2. Extraction
`entity_link_error`, `extraction_error`, `invalid_support_span`,
`normalization_error`, `taxonomy_mismatch`

Upstream. Membatasi ceiling P1 tetapi bukan bukti routing buruk.

### 3. Conflict state
`conflict_state_error`, `temporal_mismatch`, `insufficient_evidence`,
`ambiguous_gold`

State terbentuk salah walau evidence-nya benar.

### 4. Routing
`routing_error`, `unnecessary_abstention`, `unnecessary_verification`,
`unsupported_direct_answer`, `obsolete_answer`

**Hanya kelompok ini yang menjadi bukti langsung tentang kualitas P1.**

## Format catatan

Untuk setiap kasus: `request_id`, policy, action, gold outcome, kategori,
kelompok, evidence yang terlibat, dan satu kalimat mengapa kasus ini masuk
kategori tersebut.

Disimpan di `results/failure_cases/`.
