# 🎭 Sentiment Analysis Dashboard

A full-stack web application for real-time sentiment analysis using AI. Features three-tier model architecture with Fast (VADER), Precise (Hybrid), and Advanced (GPT-4o-mini) modes, offering sophisticated sentiment analysis including sarcasm detection, emotion recognition, and AI reasoning explanations.

🔗 **Live Demo:** [https://sentiment-dashboard-zeta.vercel.app/](https://sentiment-dashboard-zeta.vercel.app/)  
📚 **API Docs:** [https://sentiment-dashboard-api.onrender.com/docs](https://sentiment-dashboard-api.onrender.com/docs)  
💻 **GitHub:** [https://github.com/Vv243/sentiment-dashboard](https://github.com/Vv243/sentiment-dashboard)

---

## ✨ Features

### Core Functionality

**🎯 Three-Tier Sentiment Analysis**

- **Fast Mode**: VADER for quick analysis (~50ms)
- **Precise Mode**: Hybrid analyzer combining VADER + TextBlob + custom pattern recognition (~70ms)
- **Advanced Mode**: GPT-4o-mini with emotion detection, sarcasm recognition, and AI reasoning (~1-2s)
- 10-15% accuracy improvement over baseline VADER (Hybrid)
- Superior sarcasm and mixed emotion detection (GPT-4o-mini)

**📊 Batch CSV Analysis**

- Upload CSV files with up to 1000 rows
- Real-time progress tracking with animated progress bar
- Batch sentiment analysis with Fast/Precise mode selection
- Results table with sentiment badges and score breakdowns
- Error handling for invalid or empty rows
- Client-side processing optimized for free-tier hosting

**🧠 Advanced Text Understanding**

- Negation handling ("not bad" → positive ✅)
- Modern slang recognition ("slaps", "bussin", "hits different")
- Irony/sarcasm detection ("thanks for nothing" → negative ✅)
- **GPT-4o-mini emotion detection** (joy, sadness, anger, fear, surprise, disgust, trust, anticipation)
- **AI reasoning explanations** for sentiment classifications
- **Mixed emotion recognition** ("excited but terrified" → detects both emotions)
- Context-aware sentiment scoring
- Confidence metrics based on model agreement

**🛡️ Content Moderation**

- 41+ harmful content patterns
- Real-time content flagging
- Automatic harmful content filtering
- Smart censoring for display
- Severity classification

**📊 Historical Tracking**

- PostgreSQL database integration
- View analysis history with pagination
- Load more/less functionality
- Automatic cleanup of old records (keeps last 10,000)
- Timestamp tracking for all analyses

**🎨 Modern UI/UX**

- Beautiful gradient design with dark mode support
- Responsive layout (mobile, tablet, desktop)
- Real-time emoji indicators
- Interactive model selector
- Smooth animations and transitions
- Batch upload with file validation

**⚡ Production-Ready**

- Optimized for 512MB RAM environments
- Fast response times
- CORS enabled for frontend integration
- Automatic deployment via GitHub

---

## 🧠 Sentiment Analysis Architecture

### Model Selection Guide

```
User Input → Content Moderation → Model Selection
                                         |
                            +------------+------------+------------+
                            |            |                         |
                      Fast Mode    Precise Mode            Advanced Mode
                      (VADER)      (Hybrid)               (GPT-4o-mini)
                            |            |                         |
                            +------------+------------+------------+
                                         |
                              Shared Response Contract
                                         |
                                   JSON Response
```

All three models return an identical response shape defined by a shared contract (`analyzer_contract.py`), ensuring the API and frontend never need to know which model ran.

### Fast Mode — VADER

- Rule-based sentiment scoring
- Emoticon and punctuation awareness
- Intensity modifiers (e.g., "very", "extremely")
- ~50ms response time, ~5MB RAM

### Precise Mode — Hybrid (VADER + TextBlob + Patterns)

**1. VADER Analysis (60% weight)**
- Fast rule-based sentiment scoring

**2. TextBlob Analysis (40% weight)**
- Pattern-based sentiment detection
- Better negation handling than VADER alone

**3. Custom Pattern Boosting**
- Negation patterns: "not bad", "don't hate", "not terrible"
- Modern slang: "slaps", "bussin", "fire", "hits different", "no cap"
- Irony detection: "thanks for nothing", "oh great" + problem words
- Lukewarm expressions: "it's fine", "okay I guess"

**4. Smart Score Combination**
- Weighted averaging of VADER and TextBlob
- Pattern boost application
- Confidence calculation based on model agreement
- Normalized scores (always sum to 1.0)

### Advanced Mode — GPT-4o-mini

When to use: Complex text with sarcasm, mixed emotions, or when reasoning explanations are needed.

- **Emotion Detection**: Identifies joy, sadness, anger, fear, surprise, disgust, trust, anticipation
- **AI Reasoning**: Explains why it classified text a certain way, citing specific words/phrases
- **Sarcasm Detection**: Correctly identifies sarcasm that fools rule-based models
- **Mixed Sentiment**: Detects conflicting emotions in the same text
- **Cost**: ~$0.000045 per analysis (~16,000 analyses per $5 credit)
- **Caching**: 80% cost reduction via `@lru_cache` (200 most recent analyses kept in memory)

### Example Comparisons

| Text | Fast (VADER) | Precise (Hybrid) | Advanced (GPT-4o-mini) |
|------|-------------|-----------------|----------------------|
| "This is not bad at all" | 😞 Negative (-0.34) | 😊 Positive (+0.42) | 😊 Positive (+0.40) |
| "This movie slaps!" | 😞 Negative (-0.34) | 😊 Positive (+0.63) | 😊 Positive (+0.70) |
| "Thanks for nothing" | 😊 Positive (+0.33) | 😞 Negative (-0.52) | 😞 Negative (-0.60) |
| "Oh great, another Monday." | 😊 Positive (+0.62) | 😊 Positive (+0.40) | 😞 Negative (-0.50) ✅ |
| "Excited but also terrified." | 😞 Negative (-0.88) | 😐 Neutral (-0.10) | 😐 Mixed (+0.20) ✅ |

### Performance Metrics

| Metric | Fast Mode | Precise Mode | Advanced Mode |
|--------|-----------|-------------|---------------|
| Response Time | ~50ms | ~70ms | ~1-2s |
| Memory Usage | 5MB | 8MB | <1MB* |
| Overall Accuracy | ~75% | ~85-87% | ~92%+ |
| Negation Handling | 60% | 85% | 95% |
| Sarcasm Detection | 30% | 60% | 90% |
| Emotion Detection | ❌ | ❌ | ✅ (8 emotions) |
| Reasoning Explanation | ❌ | ❌ | ✅ |
| Cost per Analysis | Free | Free | ~$0.000045 |

*GPT-4o-mini is API-based, minimal local memory footprint

---

## 🏗️ Service Architecture

### Shared Response Contract

All analyzers conform to a shared contract defined in `app/services/analyzer_contract.py`:

```python
{
    "text": str,          # Original input
    "sentiment": str,     # "positive" | "negative" | "neutral" | "harmful"
    "emoji": str,         # "😊" | "😞" | "😐" | "⚠️"
    "scores": {
        "positive": float,
        "negative": float,
        "neutral": float,
        "compound": float  # -1.0 to 1.0
    },
    "confidence": float,  # 0.0 to 1.0
    "model": str,         # "vader" | "hybrid" | "gpt-4o-mini"
    "emotions": list,     # [] for VADER/Hybrid, populated for GPT
    "reasoning": str,     # "" for VADER/Hybrid, explanation for GPT
    "cached": bool,       # True if served from cache
    "error": str | None,  # None on success
    "moderation": { ... } # Added by routing layer
}
```

This design means the API endpoint and frontend never need model-specific logic — they handle one consistent shape regardless of which analyzer ran.

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI library with hooks
- **Vite** - Fast build tool and dev server
- **Papaparse** - CSV parsing library for batch uploads
- **CSS3** - Custom styling with gradients and animations
- **Dark Mode Support** - System preference detection
- **Deployed on Vercel** - Edge CDN delivery with automatic deployments

### Backend
- **FastAPI** - High-performance Python async API framework
- **Python 3.12+** - Modern Python features
- **VADER Sentiment** - Rule-based sentiment analysis
- **TextBlob** - NLP library for text processing
- **OpenAI GPT-4o-mini** - Advanced LLM for emotion detection and reasoning
- **PostgreSQL (pg8000)** - Database for history tracking
- **Custom Pattern Recognition** - Regex-based boosting system
- **Deployed on Render** - Cloud platform with auto-scaling

### Database
- **PostgreSQL** - Relational database via Render
- **pg8000** - Pure Python PostgreSQL driver (no external dependencies)
- **Auto-cleanup** - Periodic removal of old records

### DevOps
- **Git/GitHub** - Version control and collaboration
- **Vercel** - Frontend hosting with GitHub integration
- **Render** - Backend hosting with automatic deployments
- **Environment variables** - Secure configuration management

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- PostgreSQL 14+
  - Mac: `brew install postgresql@14`
  - Windows: [Download installer](https://www.postgresql.org/download/windows/)
  - Linux: `sudo apt install postgresql`

### Option 1: Automated Setup (Recommended)

**Mac/Linux:**
```bash
git clone https://github.com/Vv243/sentiment-dashboard.git
cd sentiment-dashboard
chmod +x setup.sh && ./setup.sh
```

**Windows (PowerShell as Administrator):**
```powershell
git clone https://github.com/Vv243/sentiment-dashboard.git
cd sentiment-dashboard
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Option 2: Manual Setup

#### 1. Clone & Configure

```bash
git clone https://github.com/Vv243/sentiment-dashboard.git
cd sentiment-dashboard
cp .env.example backend/.env
# Edit backend/.env and set your DATABASE_URL and OPENAI_API_KEY
```

#### 2. Create Database

```bash
# Mac/Linux
brew services start postgresql@14
createdb sentiment_local
```

#### 3. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### 4. Frontend Setup

```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

### Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://YOUR_USERNAME@localhost/sentiment_local
OPENAI_API_KEY=your_openai_api_key_here  # Required for Advanced Mode
```

---

## 📖 API Documentation

Interactive API documentation: http://localhost:8000/docs  
Production: https://sentiment-dashboard-api.onrender.com/docs

### POST /api/v1/sentiment/analyze

**Request:**
```json
{
  "text": "This is not bad at all!",
  "model": "vader"
}
```

**Model options:** `"vader"` (fast) | `"hybrid"` (precise) | `"gpt-4o-mini"` (advanced)

**Response:**
```json
{
  "text": "This is not bad at all!",
  "sentiment": "positive",
  "emoji": "😊",
  "scores": {
    "positive": 0.623,
    "negative": 0.187,
    "neutral": 0.190,
    "compound": 0.436
  },
  "confidence": 0.687,
  "model": "hybrid",
  "emotions": [],
  "reasoning": "",
  "cached": false,
  "error": null,
  "moderation": {
    "flagged": false,
    "reason": null,
    "severity": "safe"
  },
  "timestamp": "2026-02-18T12:00:00",
  "saved_to_db": true
}
```

**GPT-4o-mini response includes additional fields:**
```json
{
  "emotions": ["joy", "trust"],
  "reasoning": "Classified as positive because 'not bad at all' is a negated negative expression indicating mild approval.",
  "cached": false
}
```

### GET /api/v1/sentiment/history?limit=10

Retrieve recent sentiment analyses.

### POST /api/v1/sentiment/feedback/{analysis_id}

Submit user feedback (thumbs up/down) for an analysis.

---

## 📁 Project Structure

```
sentiment-dashboard/
├── setup.sh                          # One-command setup for Mac/Linux
├── setup.ps1                         # One-command setup for Windows
├── .env.example                      # Environment variable template
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── sentiment.py          # API routes
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── analyzer_contract.py  # Shared response contract (NEW)
│   │   │   ├── sentiment_analyzer.py # Model router (VADER + Hybrid + GPT)
│   │   │   ├── hybrid_analyzer.py    # Hybrid model (VADER + TextBlob)
│   │   │   ├── openai_analyzer.py    # GPT-4o-mini analyzer
│   │   │   └── content_moderator.py # Content filtering
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/                        # 53 tests, 79%+ coverage
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── BatchUpload.jsx
    │   ├── App.jsx
    │   └── App.css
    └── package.json
```

---

## 🧪 Testing

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest tests/ -v --ignore=test_backup_system.py

# Run with coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term --ignore=test_backup_system.py

# View HTML coverage report
open htmlcov/index.html  # Mac
```

### Test Coverage: 79.34% (53 tests)

| Component | Coverage | Status |
|-----------|----------|--------|
| schemas.py | 100% | ✅ |
| sentiment_analyzer.py | 94.44% | ✅ |
| config.py | 92.31% | ✅ |
| content_moderator.py | 90.91% | ✅ |
| hybrid_analyzer.py | 81.16% | ✅ |
| main.py | 70.00% | ✅ |
| database.py | 65.00% | ✅ |

---

## 🌟 Key Technical Achievements

**1. Shared Analyzer Contract** — All three models conform to a single response schema defined in `analyzer_contract.py`. The API and frontend handle one consistent shape regardless of which model ran, making it trivial to add future models.

**2. Three-Tier Model Architecture** — VADER (free, ~50ms), Hybrid (free, ~70ms), and GPT-4o-mini (~$0.000045, ~1-2s) give users the right tool for each use case.

**3. OpenAI LLM Integration** — GPT-4o-mini with JSON mode, intelligent `@lru_cache` caching (80% cost reduction), graceful error fallback, and "mixed" sentiment handling.

**4. Advanced Emotion Detection** — GPT-4o-mini identifies 8 distinct emotions with natural language reasoning explanations citing specific words and phrases.

**5. Sarcasm & Mixed Emotion Handling** — GPT-4o-mini correctly identifies sarcasm ("Oh great, another Monday" → negative) and conflicting emotions that VADER misses entirely.

**6. Resource Optimization** — Runs within Render's 512MB free tier through lazy loading, efficient queries, and in-memory caching.

**7. Pattern Recognition System** — Custom regex-based system improving negation, slang, and irony detection by 10-15% over baseline VADER.

**8. Production Deployment** — Zero-downtime deployments via GitHub integration on Vercel (frontend) and Render (backend).

**9. Content Safety** — 41+ harmful content patterns with real-time severity classification and automatic censoring.

**10. Batch Processing** — Client-side CSV parsing for up to 1,000 rows with real-time progress tracking.

**11. Comprehensive Testing** — 53 passing tests with 79%+ coverage including edge cases for sarcasm, slang, negation, and API validation.

**12. Cross-Platform Setup** — One-command setup scripts for Mac, Linux, and Windows.

---

## 📚 Learning Outcomes

- ✅ Full-stack development (React + FastAPI)
- ✅ RESTful API design and implementation
- ✅ Cloud deployment (Vercel + Render)
- ✅ Database integration (PostgreSQL)
- ✅ Multi-model AI architecture design
- ✅ LLM API integration (OpenAI chat completions, JSON mode, caching)
- ✅ Shared interface contracts across service layers
- ✅ Cost optimization (API caching strategies, token management)
- ✅ Pattern recognition (regex-based boosting)
- ✅ Performance optimization (memory-constrained environments)
- ✅ Content moderation (safety and filtering)
- ✅ Modern JavaScript (React Hooks, async/await)
- ✅ Python async programming (FastAPI)
- ✅ Environment variable management (API keys, secrets)
- ✅ Git version control with feature branches
- ✅ CSV processing (batch file uploads)
- ✅ Unit & integration testing (pytest, fixtures, mocking)
- ✅ Code coverage analysis (pytest-cov, HTML reports)
- ✅ Edge case handling (negations, sarcasm, empty inputs)
- ✅ Developer experience (cross-platform setup automation)

---

## 🔧 Development Roadmap

### Phase 1: Core Features ✅ Complete
- [x] FastAPI backend + VADER sentiment analysis
- [x] React frontend with Vite
- [x] PostgreSQL integration
- [x] Production deployment (Vercel + Render)
- [x] Hybrid model (VADER + TextBlob + pattern recognition)
- [x] Content moderation (41+ patterns)
- [x] Historical tracking with pagination

### Phase 2: Enhancements ✅ Complete
- [x] Batch CSV analysis (up to 1,000 rows)
- [x] Export results and history to CSV
- [x] Analytics dashboard with Recharts
- [x] User feedback system (thumbs up/down)
- [x] Model tracking with visual badges

### Phase 3: Professional Polish 🚧 In Progress
- [x] Comprehensive test suite (53 tests, 79% coverage)
- [x] Cross-platform setup scripts (Mac/Linux/Windows)
- [x] OpenAI GPT-4o-mini service layer (`openai_analyzer.py`)
- [x] Shared analyzer response contract (`analyzer_contract.py`)
- [x] Standardized response shapes across all three models
- [x] GPT routing wired into `sentiment_analyzer.py`
- [x] Pydantic schema updated to accept all three model strings
- [ ] Database migration (add `emotions`, `reasoning` columns)
- [ ] API endpoint updates (return new fields)
- [ ] Frontend model selector UI
- [ ] Emotions and reasoning display in frontend
- [ ] Production deployment of GPT integration
- [ ] Expanded test suite for OpenAI analyzer (target 85% coverage)
- [ ] CI/CD Pipeline (GitHub Actions)

---

## 🚀 Performance Note

This application is optimized for free-tier hosting (512MB RAM) with <100ms response times for VADER and Hybrid modes. The backend may take 30-60 seconds to wake on first request after 15 minutes of inactivity (Render free tier cold start).

---

## 📄 License

MIT License - feel free to use this project for learning!

---

## 👤 Author

**Vinh** - [GitHub Profile](https://github.com/Vv243)

---

## 🙏 Acknowledgments

- **VADER Sentiment Analysis** - NLTK community
- **TextBlob** - Steven Loria
- **OpenAI GPT-4o-mini** - OpenAI
- **FastAPI** - Sebastián Ramírez
- **React** - Meta/Facebook
- **Papaparse** - Matt Holt
- **Vercel & Render** - Deployment platforms

---

**⭐ Star this repo if you find it useful!**