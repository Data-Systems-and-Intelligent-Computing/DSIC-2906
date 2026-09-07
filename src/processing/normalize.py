"""Normalisasi nilai dan nama entitas.

Normalisasi dijalankan sebelum pembandingan nilai; tanpa ini, perbedaan
penulisan akan terbaca sebagai konflik palsu.
"""
import re
import unicodedata

_PUNCT = re.compile(r"[^\w\s]", flags=re.UNICODE)
_SPACES = re.compile(r"\s+")

# Prefiks administratif yang tidak membedakan entitas.
NAME_PREFIXES = ("desa wisata", "kampung wisata", "pokdarwis", "objek wisata")


def normalize_text(value):
    if value is None:
        return None
    text = unicodedata.normalize("NFKD", str(value)).casefold()
    text = _PUNCT.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def normalize_name(value, prefixes=NAME_PREFIXES):
    """Kunci nama untuk entity linking."""
    text = normalize_text(value)
    if text is None:
        return None
    for prefix in prefixes:
        if text.startswith(prefix + " "):
            text = text[len(prefix) + 1 :]
            break
    return text.strip()


def normalize_value(value, vocabulary=None):
    """Normalisasi nilai atribut.

    vocabulary memetakan varian penulisan ke nilai kanonik dan wajib dibekukan
    sebelum held-out (perubahan setelahnya mengubah conflict state).
    """
    text = normalize_text(value)
    if text is None:
        return None
    if vocabulary:
        return vocabulary.get(text, text)
    return text
