from analysis.baseline import compare_to_baseline, compute_baseline
from analysis.features import analyze_text
from backend.database import get_user_entries, save_entry


def main() -> None:
    user_id = "demo-user"
    text = "I will study vision engineering today and prepare for my interview."

    history_before = get_user_entries(user_id)
    features = analyze_text(text)
    baseline = compute_baseline(history_before)
    comparison = compare_to_baseline(features, baseline) if history_before else []
    entry_id = save_entry(user_id, text, features)

    print("MoodMirror local MVP: OK")
    print(f"Created Entry: {entry_id}")
    print("Features:")
    for key, value in features.items():
        print(f"  {key}: {value}")

    if comparison:
        print("Compared with personal baseline:")
        for row in comparison:
            print(row)
    else:
        print("No prior history yet; this entry starts the personal baseline.")


if __name__ == "__main__":
    main()
