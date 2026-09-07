"""Inter-annotator agreement (Cohen's kappa)."""


def cohen_kappa(labels_a, labels_b):
    """Kappa untuk dua anotator pada item yang sama dan berurutan."""
    if len(labels_a) != len(labels_b):
        raise ValueError("Kedua daftar label harus sama panjang")
    n = len(labels_a)
    if n == 0:
        return None

    observed = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n

    categories = set(labels_a) | set(labels_b)
    expected = sum(
        (labels_a.count(c) / n) * (labels_b.count(c) / n) for c in categories
    )
    if expected == 1:
        # Kedua anotator memakai satu kategori saja: kappa tidak terdefinisi.
        return None
    return (observed - expected) / (1 - expected)


def agreement_report(pairs):
    """pairs: iterable of (label_a, label_b)."""
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    n = len(a)
    return {
        "n": n,
        "observed_agreement": (sum(1 for x, y in zip(a, b) if x == y) / n) if n else None,
        "cohen_kappa": cohen_kappa(a, b),
    }
