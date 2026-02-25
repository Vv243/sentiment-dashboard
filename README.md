# Sentiment Analysis Dashboard

A production full-stack web application for AI-powered sentiment analysis. Features a three-tier model architecture — Fast (VADER), Precise (Hybrid VADER+TextBlob), and Advanced (GPT-4o-mini) — with emotion detection, sarcasm recognition, AI reasoning explanations, and a full analytics suite.

**Live Demo:** https://sentiment-dashboard-zeta.vercel.app  
**API Docs:** https://sentiment-dashboard-api.onrender.com/docs  
**GitHub:** https://github.com/Vv243/sentiment-dashboard

---

## Features

### Three-Tier Sentiment Analysis

| Mode | Model | Speed | Cost | Best For |
|------|-------|-------|------|----------|
| ⚡ Fast | VADER | ~50ms | Free | Simple, high-volume text |
| 🎯 Precise | Hybrid VADER+TextBlob | ~200ms | Free | Negations, slang, irony |
| 🧠 AI | GPT-4o-mini | ~1-2s | ~$0.000045/call | Sarcasm, mixed emotions, nuance |

**Model comparison on real examples:**

| Text | ⚡ Fast (VADER) | 🎯 Precise (Hybrid) | 🧠 AI (GPT-4o-mini) |
|------|----------------|---------------------|----------------------|
| "This is not bad at all" | Negative (-0.34) | Positive (+0.42) | Positive (+0.40) |
| "That concert slapped, no cap" | Negative (-0.34) | Positive (+0.63) | Positive (+0.70) |
| "Thanks for nothing" | Positive (+0.33) | Negative (-0.52) | Negative (-0.60) |
| "Oh great, another Monday." | Positive (+0.62) | Positive (+0.40) | **Negative (-0.50)** |
| "Excited but also terrified." | Negative (-0.88) | Neutral (-0.10) | **Mixed (+0.20) [joy, fear]** |

### Full Feature Set

- **Interactive examples** — 6 curated sample texts that auto-select the best model, instantly showcasing each model's strengths
- **Emotion detection** — 8 emotions (joy, sadness, anger, fear, surprise, disgust, trust, anticipation) via GPT
- **AI reasoning explanations** — GPT explains which words drove its classification
- **LRU caching** — 80% OpenAI API cost reduction (~$0.26 total for 3 months of live demo usage)
- **Batch CSV processing** — upload up to 1,000 rows, track progress in real-time
- **Analytics dashboard** — 4 KPI cards, sentiment distribution chart, trend over time, model comparison
- **User feedback** — thumbs up/down on any analysis result
- **Content moderation** — 41+ harmful pattern detection with severity classification
- **PostgreSQL history** — full analysis history with CSV export
- **Graceful fallback** — app continues working if OpenAI API is unavailable

---

## Architecture

### Analyzer Contract Pattern

All three models return an identical response shape defined in `analyzer_contract.py`. The API layer and frontend never need to know which model ran — they handle one consistent contract regardless:

```
User Input
    |
    v
Content Moderation (41+ patterns)
    |
    v
Model Router (sentiment_analyzer.py)
    |
    +---> VADER -------+
    |                  |
    +---> Hybrid ------+---> Shared Response Contract ---> JSON Response
    |                  |
    +---> GPT-4o-mini -+
```

**Response contract shape:**
```python
{
    "text": str,
    "sentiment": "positive" | "negative" | "neutral" | "harmful",
    "emoji": "😊" | "😞" | "😐" | "⚠️",
    "scores": {
        "positive": float,   # 0.0 to 1.0
        "negative": float,   # 0.0 to 1.0
        "neutral": float,    # 0.0 to 1.0
        "compound": float    # -1.0 to 1.0
    },
    "confidence": float,
    "model": "vader" | "hybrid" | "gpt-4o-mini",
    "emotions": list,        # populated by GPT only
    "reasoning": str,        # populated by GPT only
    "cached": bool,
    "error": str | None,
    "moderation": { "flagged": bool, "reason": str, "severity": str }
}
```

This design means adding a 4th model only requires implementing the contract — nothing else changes.

### Precise Mode — Hybrid Analyzer

1. **VADER** (60% weight) — rule-based scoring
2. **TextBlob** (40% weight) — pattern-based detection, better negation handling
3. **Custom pattern boosting** — negations ("not bad"), slang ("slaps", "bussin"), irony ("thanks for nothing"), lukewarm expressions ("it's fine I guess")
4. **Weighted score combination** with confidence based on model agreement

### Advanced Mode — GPT-4o-mini

- JSON mode forces structured output (no preamble, no hallucinated keys)
- `temperature=0.1` for near-deterministic, consistent results
- `@lru_cache(maxsize=200)` keyed on MD5 hash of normalized text
- Graceful fallback to error response on API failure

---

## Tech Stack

**Backend:** Python 3.13, FastAPI, PostgreSQL (pg8000), VADER, TextBlob, OpenAI SDK  
**Frontend:** React 18, Vite, Recharts, Papaparse  
**Testing:** pytest, unittest.mock — 62 tests, 100% pass rate  
**Deployed:** Render (backend, free tier 512MB RAM) + Vercel (frontend)

---

## Project Structure

```
sentiment-dashboard/
├── setup.ps1                        # Windows one-command setup
├── setup.sh                         # Mac/Linux one-command setup
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── requirements.txt
│   ├── .env                         # DATABASE_URL, OPENAI_API_KEY (gitignored)
│   ├── app/
│   │   ├── main.py                  # FastAPI app, CORS, startup/shutdown
│   │   ├── database.py              # PostgreSQL connection + table creation
│   │   ├── api/
│   │   │   └── sentiment.py         # All endpoints: /analyze /history /feedback
│   │   ├── models/
│   │   │   └── schemas.py           # Pydantic: SentimentRequest, SentimentResponse
│   │   ├── services/
│   │   │   ├── analyzer_contract.py # Shared response schema + helper functions
│   │   │   ├── sentiment_analyzer.py# Model router
│   │   │   ├── openai_analyzer.py   # GPT-4o-mini + LRU cache
│   │   │   ├── hybrid_analyzer.py   # VADER + TextBlob + custom patterns
│   │   │   └── content_moderator.py # 41+ harmful pattern detection
│   │   └── core/
│   │       └── config.py            # Settings from env vars
│   └── tests/
│       ├── conftest.py              # Shared fixtures
│       ├── test_api_endpoints.py    # 17 tests
│       ├── test_content_moderator.py# 4 tests
│       ├── test_database.py         # 8 tests
│       ├── test_hybrid_analyzer.py  # 10 tests
│       ├── test_main.py             # 4 tests
│       ├── test_sentiment_analyzer.py # 10 tests
│       └── test_openai_analyzer.py  # 9 tests (all mocked, zero API spend)
│
└── frontend/
    ├── package.json
    ├── .env                         # VITE_API_URL
    └── src/
        ├── App.jsx                  # Model selector, sample texts, analyze form, results, history
        ├── App.css
        └── components/
            ├── Analytics.jsx        # Recharts dashboard
            ├── BatchUpload.jsx      # CSV batch processing
            ├── SentimentChart.jsx
            ├── SentimentGauge.jsx
            ├── StatsCards.jsx
            └── TrendingList.jsx
```

---

## Database Schema

**Table: `sentiment_analyses`**

| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| text | TEXT | Input text |
| sentiment | VARCHAR(50) | positive / negative / neutral / harmful |
| emoji | VARCHAR(10) | 😊 😞 😐 ⚠️ |
| positive | REAL | 0.0–1.0 |
| negative | REAL | 0.0–1.0 |
| neutral | REAL | 0.0–1.0 |
| compound | REAL | -1.0–1.0 |
| timestamp | TIMESTAMP | |
| flagged | BOOLEAN | |
| moderation_reason | TEXT | |
| moderation_severity | VARCHAR(20) | safe / low / medium / high |
| user_feedback | VARCHAR(10) | positive / negative |
| model | VARCHAR(50) | vader / hybrid / gpt-4o-mini |
| emotions | TEXT | JSON string e.g. '["joy","fear"]' |
| reasoning | TEXT | GPT explanation |

---

## API Reference

Base URL: `https://sentiment-dashboard-api.onrender.com/api/v1/sentiment`

### POST /analyze

Analyze text with a chosen model.

**Request:**
```json
{
  "text": "I love this product!",
  "model": "vader | hybrid | gpt-4o-mini"
}
```

**Response:**
```json
{
  "text": "I love this product!",
  "sentiment": "positive",
  "emoji": "😊",
  "scores": { "positive": 0.677, "negative": 0.0, "neutral": 0.323, "compound": 0.677 },
  "confidence": 0.9,
  "model": "vader",
  "emotions": [],
  "reasoning": "",
  "cached": false,
  "error": null,
  "moderation": { "flagged": false, "reason": null, "severity": "safe" },
  "timestamp": "2026-02-24T12:00:00",
  "saved_to_db": true
}
```

GPT-4o-mini responses additionally populate `emotions` and `reasoning`:
```json
{
  "emotions": ["joy", "trust"],
  "reasoning": "The phrase 'I love' is a strong positive indicator...",
  "cached": false
}
```

### GET /history?limit=10

Retrieve recent analyses.

### POST /feedback/{analysis_id}?feedback=positive|negative

Submit thumbs up/down rating for an analysis.

---

## Local Development

### Prerequisites

Python 3.13+, Node.js 22+, PostgreSQL, Git

### Quick Setup

**Windows:**
```powershell
.\setup.ps1
```

**Mac/Linux:**
```bash
./setup.sh
```

### Manual Setup

```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows
# source venv/bin/activate           # Mac/Linux
pip install -r requirements.txt

# Create backend/.env
# DATABASE_URL=postgresql://postgres@localhost/sentiment_local
# OPENAI_API_KEY=your_key_here

python -m uvicorn app.main:app --reload
```

```bash
# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://postgres@localhost/sentiment_local
OPENAI_API_KEY=your_openai_key_here
```

---

## Testing

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest --ignore=test_backup_system.py --tb=short
```

**Result: 62 passed, 100% pass rate**

| Test File | Tests | What It Covers |
|-----------|-------|----------------|
| test_api_endpoints.py | 17 | All HTTP endpoints, validation, error cases |
| test_sentiment_analyzer.py | 10 | Model routing, all three model paths |
| test_hybrid_analyzer.py | 10 | Negation, slang, irony, score combination |
| test_database.py | 8 | CRUD, schema, connection handling |
| test_openai_analyzer.py | 9 | GPT integration (fully mocked, zero API spend) |
| test_main.py | 4 | App startup, CORS, health check |
| test_content_moderator.py | 4 | Harmful pattern detection, severity levels |

**Key testing decisions:**
- All 9 OpenAI tests use `unittest.mock` — CI never makes real API calls, zero cost
- `_cached_analyze.cache_clear()` fixture prevents cross-test contamination from lru_cache
- Edge cases covered: negation handling ("not bad" → positive), empty input, invalid model string

---

## Key Technical Decisions

**Why pivot from DistilBERT to Hybrid?**  
DistilBERT requires ~268MB to load. Render's free tier provides 512MB total RAM. After accounting for Python runtime and FastAPI overhead, DistilBERT caused OOM crashes on every cold start. The Hybrid approach achieves 85-87% accuracy within the memory constraint — and the pivot itself became a meaningful engineering talking point.

**Why use an analyzer contract?**  
Without a shared contract, each new model requires updating the API endpoint, the Pydantic schema, the frontend result card, and the database insert — four touch points per model. With the contract, adding a 4th model requires only implementing one interface. The frontend and database never change.

**Why MD5 hash for cache keys?**  
Raw strings as cache keys are memory-inefficient for long texts. MD5 produces a fixed 32-character key. Normalization (lowercase + strip) before hashing means "I LOVE THIS" and "i love this" hit the same cache entry.

---

## Development History

### Phase 1 — Core (Complete)
- FastAPI backend + VADER sentiment analysis
- React frontend with Vite
- PostgreSQL integration
- Production deployment (Vercel + Render)
- Content moderation (41+ patterns)
- Historical tracking with pagination

### Phase 2 — Enhancements (Complete)
- Batch CSV analysis (up to 1,000 rows)
- Export history to CSV
- Analytics dashboard with Recharts
- User feedback system (thumbs up/down)
- Model tracking with visual badges

### Phase 3 — AI Integration (Complete)
- OpenAI GPT-4o-mini integration with emotion detection + reasoning
- Shared analyzer contract across all three models
- LRU caching layer (80% cost reduction)
- Frontend model selector UI, emotion pills, reasoning card
- Database schema migration (emotions, reasoning, model columns)
- Comprehensive test suite (62 tests, 100% pass rate)
- Cross-platform setup scripts (Mac/Linux/Windows)
- Full production deployment of GPT integration

### Phase 4 — Polish & Stability (Complete)
- Interactive sample texts — 6 curated examples with auto model selection
- 60s fetch timeout with helpful cold start error message
- PostgreSQL database upgrade and schema migration on Render
- Removed legacy environment variables and unused code
- Production bug fixes: saved_to_db, OPENAI_API_KEY, schema mismatch

---

## Performance Notes

- VADER and Hybrid modes respond in under 200ms
- GPT-4o-mini averages 1-2s (network dependent)
- Backend cold start on Render free tier: 30-60 seconds after 15 minutes of inactivity
- LRU cache holds 200 most recent unique analyses in memory; resets on server restart

---

## Author

**Vinh Pham** — [github.com/Vv243](https://github.com/Vv243) | [linkedin.com/in/vinhpham243](https://linkedin.com/in/vinhpham243)

---

## Acknowledgments

VADER (NLTK community) · TextBlob (Steven Loria) · OpenAI GPT-4o-mini · FastAPI (Sebastián Ramírez) · React (Meta) · Papaparse (Matt Holt) · Vercel · Render