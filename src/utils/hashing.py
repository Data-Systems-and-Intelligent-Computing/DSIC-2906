"""Checksum untuk provenance snapshot mentah."""
import hashlib


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def sha256_text(text, encoding="utf-8"):
    return sha256_bytes(text.encode(encoding))


def sha256_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()
