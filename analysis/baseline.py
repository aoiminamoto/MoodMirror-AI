from typing import Dict, List


def build_baseline(previous_entries: List[dict]) -> Dict[str, float]:
    if not previous_entries:
        return {}

    metric_names = [
        "word_count",
        "lexical_diversity",
        "avg_sentence_length",
        "question_ratio",
        "exclamation_ratio",
        "future_orientation",
        "uncertainty",
        "action_orientation",
    ]

    baseline = {}

    for metric in metric_names:
        values = []

        for entry in previous_entries:
            value = entry.get(metric)
            if value is not None:
                values.append(float(value))

        if values:
            baseline[metric] = sum(values) / len(values)

    return baseline


def compare_with_baseline(
    current_features: Dict[str, float],
    previous_entries: List[dict],
):
    baseline = build_baseline(previous_entries)

    if not baseline:
        return []

    results = []

    for metric, current in current_features.items():
        if metric not in baseline:
            continue

        base = baseline[metric]

        if base == 0:
            percent_change = None
        else:
            percent_change = round(
                ((current - base) / base) * 100,
                2,
            )

        results.append(
            {
                "metric": metric,
                "current": current,
                "baseline": round(base, 4),
                "percent_change": percent_change,
            }
        )

    return results