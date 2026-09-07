"""Paired bootstrap.

Unit resampling adalah ENTITY, bukan article atau claim row: beberapa request
dari satu entitas tidak independen, dan resampling per baris akan membuat
confidence interval terlalu sempit.
"""
import random


def group_by_entity(results):
    groups = {}
    for r in results:
        groups.setdefault(r.get("entity_id"), []).append(r)
    return groups


def paired_bootstrap(baseline, treatment, statistic, iterations=10000, seed=42, alpha=0.05):
    """CI bootstrap untuk selisih statistic(treatment) - statistic(baseline).

    Kedua policy diresample pada entitas yang SAMA di tiap iterasi, sehingga
    desainnya tetap berpasangan.
    """
    base_groups = group_by_entity(baseline)
    treat_groups = group_by_entity(treatment)
    entities = sorted(set(base_groups) & set(treat_groups))
    if not entities:
        raise ValueError("Tidak ada entity yang sama antara baseline dan treatment")

    rng = random.Random(seed)
    deltas = []
    for _ in range(iterations):
        sample = [entities[rng.randrange(len(entities))] for _ in entities]
        b_rows, t_rows = [], []
        for e in sample:
            b_rows.extend(base_groups[e])
            t_rows.extend(treat_groups[e])
        b_stat, t_stat = statistic(b_rows), statistic(t_rows)
        if b_stat is None or t_stat is None:
            continue
        deltas.append(t_stat - b_stat)

    if not deltas:
        return {"point": None, "ci_low": None, "ci_high": None, "n_entities": len(entities)}

    deltas.sort()
    lo = deltas[int((alpha / 2) * len(deltas))]
    hi = deltas[min(len(deltas) - 1, int((1 - alpha / 2) * len(deltas)))]
    b_stat, t_stat = statistic(baseline), statistic(treatment)
    point = None if (b_stat is None or t_stat is None) else t_stat - b_stat
    return {
        "point": point,
        "ci_low": lo,
        "ci_high": hi,
        "n_entities": len(entities),
        "iterations": len(deltas),
    }
