"""Metrik primer, value-of-news, dan cost.

Aturan pelaporan: accuracy tidak pernah dilaporkan sendirian. Sistem yang
abstain 100% punya risk nol dan coverage nol, sehingga risk, coverage, dan
verification harus selalu muncul bersama.
"""


def _answered(results):
    return [r for r in results if r.get("answered")]


def selective_accuracy(results):
    """correct answered / answered. None bila tidak ada yang dijawab."""
    answered = _answered(results)
    if not answered:
        return None
    return sum(1 for r in answered if r.get("correct")) / len(answered)


def selective_risk(results):
    """incorrect answered / answered."""
    answered = _answered(results)
    if not answered:
        return None
    return sum(1 for r in answered if r.get("correct") is False) / len(answered)


def answer_coverage(results):
    """answered / all requests."""
    if not results:
        return None
    return len(_answered(results)) / len(results)


def unsupported_answer_rate(results):
    """answered tanpa supported evidence / answered."""
    answered = _answered(results)
    if not answered:
        return None
    return sum(1 for r in answered if r.get("unsupported")) / len(answered)


def verification_rate(results):
    if not results:
        return None
    return sum(1 for r in results if r.get("verification_invoked")) / len(results)


def abstention_rate(results):
    if not results:
        return None
    return sum(1 for r in results if r.get("action") == "A") / len(results)


def _key(result):
    return result.get("request_id")


def _pair(baseline, treatment):
    """Pasangkan hasil dua policy berdasarkan request_id."""
    base = {_key(r): r for r in baseline}
    return [(base[_key(t)], t) for t in treatment if _key(t) in base]


def _changed(before, after):
    return (before.get("action") != after.get("action")) or (
        before.get("returned_value") != after.get("returned_value")
    )


def decision_change_rate(baseline, treatment):
    """DCR: proporsi request yang route/output-nya berubah."""
    pairs = _pair(baseline, treatment)
    if not pairs:
        return None
    return sum(1 for b, t in pairs if _changed(b, t)) / len(pairs)


def _classify_change(before, after):
    """beneficial | harmful | neutral untuk satu keputusan yang berubah."""
    was_bad = (
        before.get("correct") is False
        or before.get("unsupported")
        or before.get("obsolete")
    )
    now_bad = (
        after.get("correct") is False
        or after.get("unsupported")
        or after.get("obsolete")
    )

    # Jawaban buruk dicegah, atau jawaban benar dipulihkan.
    if was_bad and not now_bad:
        return "beneficial"
    if not before.get("answered") and after.get("answered") and after.get("correct"):
        return "beneficial"

    # Jawaban baik dirusak, atau jawaban benar hilang.
    if now_bad and not was_bad:
        return "harmful"
    if before.get("answered") and before.get("correct") and not after.get("answered"):
        return "harmful"

    # Verifikasi tambahan tanpa perubahan hasil: biaya tanpa manfaat.
    if (
        not before.get("verification_invoked")
        and after.get("verification_invoked")
        and before.get("answered") == after.get("answered")
        and before.get("correct") == after.get("correct")
    ):
        return "harmful"

    return "neutral"


def change_breakdown(baseline, treatment):
    """Hitung beneficial/harmful/neutral pada keputusan yang berubah."""
    pairs = _pair(baseline, treatment)
    changed = [(b, t) for b, t in pairs if _changed(b, t)]
    counts = {"beneficial": 0, "harmful": 0, "neutral": 0}
    for before, after in changed:
        counts[_classify_change(before, after)] += 1
    counts["changed"] = len(changed)
    counts["total"] = len(pairs)
    return counts


def beneficial_decision_change_rate(baseline, treatment):
    """BDCR: beneficial / changed. None bila tidak ada yang berubah."""
    counts = change_breakdown(baseline, treatment)
    if not counts["changed"]:
        return None
    return counts["beneficial"] / counts["changed"]


def harmful_decision_change_rate(baseline, treatment):
    counts = change_breakdown(baseline, treatment)
    if not counts["changed"]:
        return None
    return counts["harmful"] / counts["changed"]


def news_evidence_utilization_rate(results):
    """Proporsi request di mana berita eligible benar-benar dipakai."""
    if not results:
        return None
    return sum(1 for r in results if r.get("news_claims_used", 0) > 0) / len(results)


def summarize(results):
    """Ringkasan satu policy. Risk selalu berpasangan dengan coverage."""
    return {
        "n_requests": len(results),
        "selective_accuracy": selective_accuracy(results),
        "selective_risk": selective_risk(results),
        "answer_coverage": answer_coverage(results),
        "unsupported_answer_rate": unsupported_answer_rate(results),
        "verification_rate": verification_rate(results),
        "abstention_rate": abstention_rate(results),
    }
