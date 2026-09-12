import re
from collections import Counter
from typing import Dict


FUTURE_WORDS = {
    "will", "plan", "planning", "goal", "goals", "next", "future", "prepare",
    "preparing", "learn", "learning", "build", "building", "want", "intend"
}

UNCERTAINTY_WORDS = {
    "maybe", "perhaps", "might", "could", "unsure", "uncertain", "worry",
    "worried", "guess", "possibly", "probably", "hope"
}

ACTION_WORDS = {
    "do", "doing", "make", "making", "build", "building", "study", "studying",
    "learn", "learning", "prepare", "preparing", "apply", "create", "finish",
    "complete", "practice", "work", "working"
}


def _tokens(text: str):
    return re.findall(r"[A-Za-z']+", text.lower())


def analyze_text(text: str) -> Dict[str, float]:
    """Return reproducible, non-diagnostic writing-pattern features."""
    text = (text or "").strip()
    tokens = _tokens(text)
    word_count = len(tokens)
    unique_count = len(set(tokens))

    sentence_parts = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = max(len(sentence_parts), 1)

    counts = Counter(tokens)

    def ratio(words):
        if word_count == 0:
            return 0.0
        return sum(counts[w] for w in words) / word_count

    return {
        "word_count": float(word_count),
        "lexical_diversity": round(unique_count / word_count, 4) if word_count else 0.0,
        "avg_sentence_length": round(word_count / sentence_count, 4) if word_count else 0.0,
        "question_ratio": round(text.count("?") / sentence_count, 4),
        "exclamation_ratio": round(text.count("!") / sentence_count, 4),
        "future_orientation": round(ratio(FUTURE_WORDS), 4),
        "uncertainty": round(ratio(UNCERTAINTY_WORDS), 4),
        "action_orientation": round(ratio(ACTION_WORDS), 4),
    }
