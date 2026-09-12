from typing import Dict, Iterable, List

from backend.database import FEATURE_COLUMNS


def compute_baseline(entries: Iterable[dict]) -> Dict[str, float]:
    rows = list(entries)
    if not rows:
        return {name: 0.0 for name in FEATURE_COLUMNS}

    baseline = {}
    for name in FEATURE_COLUMNS:
        values = [float(row[name]) for row in rows]
        baseline[name] = round(sum(values) / len(values), 4)
    return baseline


def compare_to_baseline(current: Dict[str, float], baseline: Dict[str, float]) -> List[dict]:
    comparisons = []
    for name in FEATURE_COLUMNS:
        current_value = float(current[name])
        baseline_value = float(baseline.get(name, 0.0))
        if baseline_value == 0:
            percent_change = None
        else:
            percent_change = round((current_value - baseline_value) / baseline_value * 100, 1)
        comparisons.append(
            {
                "metric": name,
                "current": round(current_value, 4),
                "baseline": round(baseline_value, 4),
                "percent_change": percent_change,
            }
        )
    return comparisons
