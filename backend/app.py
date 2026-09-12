from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel

from analysis.baseline import compare_with_baseline
from backend.database import Database
from backend.daytona_service import analyze_text_in_daytona


app = FastAPI(
    title="MoodMirror AI",
    description="Longitudinal writing-pattern analysis using Daytona + SQLite",
    version="0.2.0",
)

db = Database()


class AnalyzeRequest(BaseModel):
    user_id: str = "demo-user"
    text: str

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    # 1. Get prior history first
    previous_entries = db.get_entries(request.user_id)

    # 2. Run writing analysis inside Daytona sandbox
    features = analyze_text_in_daytona(request.text)

    # 3. Compare current features against previous personal baseline
    comparison = compare_with_baseline(
        current_features=features,
        previous_entries=previous_entries,
    )

    # 4. Save current entry after comparison
    entry_id = db.save_entry(
        user_id=request.user_id,
        text=request.text,
        features=features,
    )

    return {
        "entry_id": entry_id,
        "analysis_engine": "Daytona Sandbox",
        "features": features,
        "baseline_comparison": comparison,
        "history_count_before_this_entry": len(previous_entries),
    }