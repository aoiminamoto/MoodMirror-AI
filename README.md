# MoodMirror AI

**AI-powered writing pattern analysis with personalized longitudinal insights.**

Tokyo Hackathon — September 12, 2026

MoodMirror AI explores a simple idea: instead of comparing a person's writing with population-level norms, build a **personal baseline** from their own historical writing and show how their language patterns evolve over time.

## Architecture

```text
User Writing
    |
    v
MoodMirror API / Agent
    |
    +--> Daytona Sandbox --> reproducible Python/NLP analysis
    +--> Neo4j Aura ------> longitudinal personal knowledge graph
    +--> Nosana ----------> GPU inference / embeddings
    |
    v
Personal Baseline + Trends + Explainable Insights
```

## Sponsor Technology Integration

### Neo4j Aura — Longitudinal Knowledge Graph
Stores relationships between users, writing entries, topics, and writing patterns over time.

```text
(User)-[:WROTE]->(Entry)
(Entry)-[:HAS_PATTERN {score: ...}]->(Pattern)
(Entry)-[:MENTIONS]->(Topic)
```

### Daytona — Secure Agent Code Execution
Provides isolated sandboxes where MoodMirror can execute reproducible Python linguistic and statistical analysis rather than relying only on free-form LLM judgments.

### Nosana — GPU Inference
Provides compute for model inference and semantic embeddings used to compare a new entry with semantically related historical writing.

## Planned Features

- Structured writing-pattern feature extraction
- Personal baseline from historical entries
- Current-entry vs. baseline comparison
- Longitudinal trend visualization
- Neo4j personal language graph
- Semantic similarity across historical writing
- Explainable evidence behind generated insights

## Engineering Milestones

- [x] Project foundation
- [ ] Connect Neo4j Aura and create graph schema
- [ ] Execute writing analysis in a Daytona sandbox
- [ ] Store Daytona analysis results in Neo4j
- [ ] Deploy embedding/model inference with Nosana
- [ ] Add personal-baseline comparison
- [ ] Add frontend and trend visualization
- [ ] Add tests, screenshots, architecture diagram, and demo

## Repository Structure

```text
MoodMirror-AI/
├── analysis/
├── backend/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Safety / Product Scope

MoodMirror is designed for **personal reflection and exploration of writing patterns**. It does not diagnose mental-health, neurological, cognitive, or other medical conditions.

## Author

Aoi Minamoto
