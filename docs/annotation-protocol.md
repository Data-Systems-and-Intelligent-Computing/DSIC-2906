# Protokol Anotasi

## Unit

```text
entity_id x attribute x query_time
```

Satu request dinilai **as-of query_time**.

## Outcome

| Outcome | Kapan dipakai |
|---|---|
| `accepted_value` | ada nilai yang dapat diterima pada query_time |
| `unresolved_unknown` | evidence tidak cukup untuk menetapkan nilai |
| `not_applicable` | atribut tidak berlaku bagi entitas ini |

`accepted_values` boleh berisi lebih dari satu nilai bila beberapa penulisan
sama-sama benar.

## Aturan yang paling sering dilanggar tanpa sengaja

1. **Evidence setelah query_time dilarang.** Termasuk artikel yang "jelas
   benar" tetapi terbit belakangan.
2. **Berita bukan otomatis ground truth.** Berita adalah evidence.
3. **Sumber mayoritas bukan otomatis benar.** Cek lineage: tiga repost dari
   satu origin adalah satu suara.
4. **Gold tidak boleh hanya berisi konflik yang sudah diketahui.** Sertakan
   kasus clean agreement dan kasus tanpa berita.
5. **Anotator tidak melihat keluaran policy.** Formulir menolak kolom
   `action`, `policy`, `returned_value`, `conflict_label`, `correct`
   (ditegakkan di `src/annotation/export_gold_form.py`).

## Prosedur

1. Bekukan entity list, query time, source cutoff, evidence cutoff.
2. Ekspor formulir: `bash scripts/08_export_annotation.sh`.
3. Anotasi pertama pada seluruh request.
4. Anotasi kedua pada 20–25% request dan ≥20% news claim (~100 claim).
5. Hitung agreement (Cohen's kappa) per atribut.
6. Adjudikasi seluruh disagreement — wajib selesai sebelum evaluasi final.
7. Bekukan held-out: `bash scripts/09_freeze_heldout.sh`.

## Ketertelusuran

Setiap request harus dapat ditelusuri ke structured value, artikel/reference,
normalized claim, source lineage, URL, `published_at`/`observed_at`,
`fetched_at`, dan supporting span.

## Catatan tentang gold yang tidak pasti

Gold boleh `unresolved_unknown`. Memaksakan nilai pada kasus yang memang tidak
dapat ditentukan akan menghukum abstention yang sebenarnya tepat — dan
abstention yang tepat adalah bagian dari yang diteliti.
