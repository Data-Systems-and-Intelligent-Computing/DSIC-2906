"""Benchmark latency query-time.

Latency crawling dan preprocessing TIDAK termasuk: yang diukur hanya biaya
keputusan pada frozen snapshot.
"""
import random


def percentile(values, q):
    if not values:
        return None
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(round(q * (len(ordered) - 1))))
    return ordered[idx]


def summarize_latency(values):
    return {
        "n": len(values),
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }


def randomized_policy_order(policies, seed=42):
    """Urutan policy diacak per repetisi agar drift JVM/cache tidak
    sistematis menguntungkan policy yang selalu berjalan lebih dulu."""
    order = list(policies)
    random.Random(seed).shuffle(order)
    return order


def build_schedule(policies, repetitions=20, warmup=2, seed=42):
    """Jadwal eksekusi: warm-up berlabel, lalu repetisi terukur dengan
    urutan policy yang diacak per repetisi."""
    schedule = []
    for r in range(warmup):
        for p in randomized_policy_order(policies, seed + r):
            schedule.append({"policy": p, "repetition": r, "warmup": True})
    for r in range(repetitions):
        for p in randomized_policy_order(policies, seed + 1000 + r):
            schedule.append({"policy": p, "repetition": r, "warmup": False})
    return schedule
