from fastapi import FastAPI
from pydantic import BaseModel

from analysis.baseline import compare_to_baseline, compute_baseline
from analysis.features import analyze_text
from backend.database import get_user_entries, save_entry

app = FastAPI(title="MoodMirror AI", version="0.1.0")


class AnalyzeRequest(BaseModel):
    user_id: str = "demo-user"
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    history_before = get_user_entries(req.user_id)
    current = analyze_text(req.text)
    baseline = compute_baseline(history_before)
    comparison = compare_to_baseline(current, baseline) if history_before else []
    entry_id = save_entry(req.user_id, req.text, current)

    return {
        "entry_id": entry_id,
        "user_id": req.user_id,
        "features": current,
        "has_personal_baseline": bool(history_before),
        "baseline": baseline if history_before else None,
        "comparison": comparison,
        "history_count_before_current": len(history_before),
        "disclaimer": "Writing-pattern reflection only; not medical or psychological diagnosis.",
    }
