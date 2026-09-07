# Direct, Verify, or Abstain? Conflict-Aware Query Handling across Structured Records and Unstructured Tourism Evidence

## Abstract
TBD setelah held-out result dibekukan. Tulis terakhir.

## 1. Introduction
- Masalah: structured tourism record bisa usang atau bertentangan dengan
  laporan terbaru, tetapi query handling umumnya mengembalikan nilai apa adanya.
- Kontribusi (lihat `docs/publication-boundary.md`): keputusan query-time
  Direct / Verify / Abstain berbasis conflict state lintas format.
- Bukan kontribusi: extraction, fusion, truth discovery, RAG, retrieval.

## 2. Background
### 2.1 Structured tourism records dan keterbatasannya
### 2.2 Temporally anchored unstructured evidence
### 2.3 Conflict state dan selective prediction
### 2.4 Risk-coverage trade-off

## 3. Related Work
Pencarian literatur final 2021-2026; catat direct prior art sebelum
menetapkan klaim kebaruan.

## 4. Data and Testbed
### 4.1 Sumber: JADESTA, Wikidata, Wikipedia, tourism news
### 4.2 Source dependence dan story lineage
### 4.3 Candidate pool dan attribute scope
### 4.4 Lakehouse testbed (bukan kontribusi)

## 5. Method
### 5.1 Evidence claim schema dan supporting span
### 5.2 Conflict state C_S dan C_SU
### 5.3 Freshness window dan temporal eligibility
### 5.4 Policies B0, B1, B2, P1
### 5.5 Verification routine (fixed)

## 6. Experimental Setup
### 6.1 Query workload Q1-Q3
### 6.2 Held-out gold dan protokol anotasi
### 6.3 Metrik: risk, coverage, unsupported rate, DCR/BDCR, cost
### 6.4 Analisis statistik: paired bootstrap pada unit entity

## 7. Results
### 7.1 RQ1/RQ4 - perbandingan policy
### 7.2 RQ2 - transisi C_S -> C_SU
### 7.3 RQ3 - beneficial vs harmful decision change
### 7.4 RQ5 - verification cost dan latency vs B2
### 7.5 RQ6 - time-sensitive vs stable control

## 8. Failure Analysis
Pisahkan source, extraction, conflict-state, dan routing failure.

## 9. Discussion
Termasuk kasus P1 tidak mengungguli B1: hasil negatif tetap sah dan harus
dilaporkan sebagai temuan.

## 10. Threats to Validity
Source dependence, gold uncertainty, temporal leakage, stale evidence,
extraction error, entity-linking error, coverage bias, routing leakage,
systems generalization.

## 11. Conclusion

## Publication Boundary Statement
Ringkas dari `docs/publication-boundary.md`; wajib muncul di manuskrip.
