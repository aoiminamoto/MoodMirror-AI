# MoodMirror AI

**AI-powered writing pattern analysis with personalized longitudinal insights.**

Tokyo Hackathon — September 12, 2026

MoodMirror AI explores a simple idea: instead of comparing a person's writing with population-level norms, build a **personal baseline** from their own historical writing and show how their language patterns evolve over time.

## MVP Architecture

```text
User Writing
    |
    v
MoodMirror API
    |
    +--> deterministic Python writing analysis
    |
    +--> SQLite --> writing history + personal baseline
    |
    +--> Daytona Sandbox --> secure/reproducible code execution
    |
    +--> Nosana --> model inference / semantic embeddings
    |
    v
Personal Baseline + Trends + Explainable Insights
```

## Core MVP

The first working version deliberately stays simple:

1. Accept a writing entry.
2. Extract reproducible writing-pattern features in Python.
3. Store the entry locally in SQLite.
4. Build a personal baseline from the user's own history.
5. Compare a new entry with that baseline.
6. Return structured, explainable changes rather than free-form AI guesses.

Current deterministic features include:

- word count
- lexical diversity
- average sentence length
- question ratio
- exclamation ratio
- future-oriented language
- uncertainty language
- action-oriented language

## Sponsor Technology Integration

### Daytona — Secure Agent Code Execution
Planned integration: execute the same writing analysis inside an isolated Daytona sandbox so the analysis is reproducible and separated from the application host.

### Nosana — GPU Inference
Planned integration: deploy an embedding or lightweight inference endpoint for semantic similarity across historical writing entries.

## Personal Baseline

MoodMirror's key product idea is **self-comparison over time**.

```text
Entry 1 -> writing features
Entry 2 -> writing features
Entry 3 -> writing features
               |
               v
        Personal baseline
               |
               v
New entry -> current vs. baseline
```

Example output:

```text
Today vs personal baseline

Future orientation    +24%
Action orientation    +18%
Uncertainty           -13%
Lexical diversity      +7%
```

## Run the Local MVP

```bash
pip install -r requirements.txt
python -m backend.smoke_test
```

Run the API:

```bash
uvicorn backend.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Use `POST /analyze` with a request like:

```json
{
  "user_id": "demo-user",
  "text": "I will study vision engineering today and prepare for my interview."
}
```

Run tests:

```bash
pytest
```

## Repository Structure

```text
MoodMirror-AI/
├── analysis/
│   ├── features.py
│   └── baseline.py
├── backend/
│   ├── app.py
│   ├── database.py
│   └── smoke_test.py
├── tests/
│   └── test_features.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Engineering Milestones

- [x] Project foundation
- [x] Deterministic writing feature extraction
- [x] SQLite writing history
- [x] Personal baseline comparison
- [x] FastAPI analysis endpoint
- [ ] Execute analysis in Daytona sandbox
- [ ] Deploy embedding/model inference with Nosana
- [ ] Add simple frontend and trend visualization
- [ ] Add demo screenshots/video and final submission materials

## Safety / Product Scope

MoodMirror is designed for **personal reflection and exploration of writing patterns**. It does not diagnose mental-health, neurological, cognitive, or other medical conditions.

## Author

Aoi Minamoto
