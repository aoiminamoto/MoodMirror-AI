import json
from daytona import Daytona


def analyze_text_in_daytona(text: str) -> dict:
    """Run deterministic MoodMirror text analysis inside a Daytona sandbox."""

    daytona = Daytona()
    sandbox = daytona.create()

    try:
        code = f'''
import json
import re

text = {text!r}

words = re.findall(r"\\b\\w+\\b", text.lower())
sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]

word_count = len(words)
unique_words = len(set(words))
sentence_count = max(len(sentences), 1)

future_words = {{"will", "plan", "future", "next", "goal", "prepare", "learn"}}
uncertainty_words = {{"maybe", "perhaps", "unsure", "uncertain", "might", "could"}}
action_words = {{"do", "build", "make", "create", "learn", "prepare", "work"}}


def ratio(vocab):
    if not words:
        return 0.0
    return round(sum(1 for w in words if w in vocab) / len(words), 4)


features = {{
    "word_count": float(word_count),
    "lexical_diversity": round(unique_words / word_count, 4) if word_count else 0.0,
    "avg_sentence_length": round(word_count / sentence_count, 4),
    "question_ratio": round(text.count("?") / sentence_count, 4),
    "exclamation_ratio": round(text.count("!") / sentence_count, 4),
    "future_orientation": ratio(future_words),
    "uncertainty": ratio(uncertainty_words),
    "action_orientation": ratio(action_words),
}}

print(json.dumps(features))
'''

        result = sandbox.process.code_run(code)
        return json.loads(result.result.strip())

    finally:
        try:
            sandbox.delete()
        except Exception:
            pass