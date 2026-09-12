from backend.daytona_service import analyze_text_in_daytona


def main():
    text = "I will prepare for my interview and learn vision engineering today."

    features = analyze_text_in_daytona(text)

    print("Daytona MoodMirror analysis: OK")

    for key, value in features.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
