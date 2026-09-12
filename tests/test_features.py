from analysis.features import analyze_text


def test_empty_text():
    features = analyze_text("")
    assert features["word_count"] == 0.0
    assert features["lexical_diversity"] == 0.0


def test_future_and_action_language():
    features = analyze_text("I will prepare, study, learn, and build the project.")
    assert features["future_orientation"] > 0
    assert features["action_orientation"] > 0
