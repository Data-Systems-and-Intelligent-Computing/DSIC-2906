"""Entity linking.

BUKAN novelty (publication boundary), tetapi wajib auditable: setiap tautan
menyimpan metode dan skornya agar linking error dapat dipisahkan dari routing
error saat failure analysis.
"""
from difflib import SequenceMatcher

from src.processing.normalize import normalize_name

ACCEPT_THRESHOLD = 92
REVIEW_THRESHOLD = 80


def similarity(a, b):
    """Skor kemiripan 0-100 pada nama yang sudah dinormalisasi."""
    na, nb = normalize_name(a) or "", normalize_name(b) or ""
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio() * 100


def link_candidate(name, candidates, accept=ACCEPT_THRESHOLD, review=REVIEW_THRESHOLD):
    """Tautkan satu nama ke daftar kandidat.

    Mengembalikan (match, method, score) dengan method:
      exact  - kunci ternormalisasi identik, diterima otomatis
      fuzzy  - skor >= accept, diterima otomatis
      review - skor di antara review dan accept, WAJIB dilihat manusia
      none   - di bawah review threshold
    """
    key = normalize_name(name)
    for candidate in candidates:
        if normalize_name(candidate) == key:
            return candidate, "exact", 100.0

    best, best_score = None, 0.0
    for candidate in candidates:
        score = similarity(name, candidate)
        if score > best_score:
            best, best_score = candidate, score

    if best_score >= accept:
        return best, "fuzzy", best_score
    if best_score >= review:
        return best, "review", best_score
    return None, "none", best_score
