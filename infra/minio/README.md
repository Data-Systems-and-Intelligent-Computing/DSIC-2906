# MinIO — Raw Zone

Object store S3-compatible untuk raw zone dan warehouse Iceberg.

- Bucket dibuat otomatis oleh service `minio-init` (`${MINIO_BUCKET}`).
- Layout raw zone: `raw/{source_id}/{fetched_date}/{checksum}.{ext}`
  (`configs/acquisition.yaml`).

## Immutability

Raw zone bersifat **immutable**. Payload yang sudah tersimpan tidak boleh
ditimpa; akuisisi ulang menghasilkan snapshot baru dengan checksum baru.
Tanpa aturan ini, gate "Raw→Bronze→Silver→Gold replayable" dan "source
snapshots frozen" tidak dapat dibuktikan.

## Yang wajib tersimpan bersama payload

URL/reference, publisher, `published_at`, `fetched_at`, HTTP status,
discovery query, checksum SHA-256, dan story lineage. Artikel tanpa
`published_at` tidak akan pernah temporally eligible, jadi catat saat
akuisisi — bukan belakangan.
