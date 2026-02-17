# 🎭 Sentiment Analysis Dashboard

A full-stack web application for real-time sentiment analysis using AI. Features dual-model architecture with Fast (VADER) and Precise (Hybrid) modes, offering 10-15% accuracy improvement through intelligent model combination and pattern recognition.

🔗 **Live Demo:** [https://sentiment-dashboard-zeta.vercel.app/](https://sentiment-dashboard-zeta.vercel.app/)  
📚 **API Docs:** [https://sentiment-dashboard-api.onrender.com/docs](https://sentiment-dashboard-api.onrender.com/docs)  
💻 **GitHub:** [https://github.com/Vv243/sentiment-dashboard](https://github.com/Vv243/sentiment-dashboard)

---

## ✨ Features

### Core Functionality

**🎯 Dual-Model Sentiment Analysis**

- **Fast Mode**: VADER for quick analysis (~50ms)
- **Precise Mode**: Hybrid analyzer combining VADER + TextBlob + custom pattern recognition (~70ms)
- 10-15% accuracy improvement over baseline VADER

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

## 🧠 Hybrid Sentiment Analysis

The Precise mode uses a sophisticated multi-model approach:

### Architecture

```
User Input → Content Moderation → Model Selection
                                         |
                            +------------+------------+
                            |                         |
                      Fast Mode                 Precise Mode
                      (VADER only)              (Hybrid)
                            |                         |
                            +------------+------------+
                                         |
                                   JSON Response
```

### Hybrid Model Components

**1. VADER Analysis (60% weight)**

- Fast rule-based sentiment scoring
- Emoticon and punctuation awareness
- Intensity modifiers (e.g., "very", "extremely")

**2. TextBlob Analysis (40% weight)**

- Pattern-based sentiment detection
- Better negation handling than VADER
- Subjectivity scoring

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

### Example Improvements

| Text                     | Fast Mode (VADER)   | Precise Mode (Hybrid) | Winner    |
| ------------------------ | ------------------- | --------------------- | --------- |
| "This is not bad at all" | 😞 Negative (-0.34) | 😊 Positive (+0.42)   | ✅ Hybrid |
| "This movie slaps!"      | 😞 Negative (-0.34) | 😊 Positive (+0.63)   | ✅ Hybrid |
| "Thanks for nothing"     | 😊 Positive (+0.33) | 😞 Negative (-0.52)   | ✅ Hybrid |
| "It's fine I guess"      | 😊 Positive (+0.22) | 😐 Neutral (-0.05)    | ✅ Hybrid |
| "I don't hate it"        | 😞 Negative (-0.58) | 😊 Positive (+0.18)   | ✅ Hybrid |
| "I love this!"           | 😊 Positive (+0.80) | 😊 Positive (+0.85)   | Both work |

### Performance Metrics

| Metric            | Fast Mode | Precise Mode |
| ----------------- | --------- | ------------ |
| Response Time     | ~50ms     | ~70ms        |
| Memory Usage      | 5MB       | 8MB          |
| Overall Accuracy  | ~75%      | ~85-87%      |
| Negation Handling | 60%       | 85%          |
| Slang Recognition | 50%       | 80%          |
| Irony Detection   | 40%       | 70%          |
| RAM Required      | <10MB     | <10MB        |

**Tested on Render free tier (512MB RAM)**

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

The setup script will automatically:
- Check all prerequisites
- Start PostgreSQL
- Create the local database
- Set up Python virtual environment
- Install all dependencies
- Create `.env` files with correct settings

### Option 2: Manual Setup

#### 1. Clone Repository

```bash
git clone https://github.com/Vv243/sentiment-dashboard.git
cd sentiment-dashboard
```

#### 2. Configure Environment

```bash
# Copy the example env file
cp .env.example backend/.env

# Edit backend/.env and set your DATABASE_URL:
# Mac/Linux: postgresql://YOUR_USERNAME@localhost/sentiment_local
# Windows:   postgresql://postgres@localhost/sentiment_local
```

#### 3. Create Database

```bash
# Mac/Linux
brew services start postgresql@14
createdb sentiment_local

# Windows (in psql)
createdb -U postgres sentiment_local
```

#### 4. Backend Setup

```bash
cd backend
python3 -m venv venv

# Mac/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on **http://localhost:8000**

#### 5. Frontend Setup

```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

Frontend runs on **http://localhost:3000**

### Starting the Project (After Setup)

Every time you work on the project, open two terminal tabs:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate   # Mac/Linux
# .\venv\Scripts\Activate.ps1  # Windows
python -m uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

> **Note:** Make sure PostgreSQL is running first.  
> Mac: `brew services start postgresql@14`  
> Windows: PostgreSQL runs as a service automatically after install.

---

## 📖 API Documentation

Interactive API documentation available at:

- **Local:** http://localhost:8000/docs
- **Production:** https://sentiment-dashboard-api.onrender.com/docs

### Main Endpoints

#### POST /api/v1/sentiment/analyze

Analyze sentiment of input text with model selection.

**Request:**

```json
{
  "text": "This is not bad at all!",
  "model": "vader"
}
```

**Parameters:**

- `text` (required): Text to analyze (1-5000 characters)
- `model` (optional): `"vader"` (fast) or `"distilbert"` (precise/hybrid), default: `"vader"`

**Response:**

```json
{
  "text": "This is not bad at all!",
  "sentiment": "positive",
  "emoji": "😊",
  "scores": {
    "positive": 0.623,
    "negative": 0.187,
    "neutral": 0.19,
    "compound": 0.436
  },
  "confidence": 0.687,
  "model": "hybrid",
  "details": {
    "vader_score": -0.34,
    "textblob_score": 0.35,
    "pattern_boost": 0.4
  },
  "moderation": {
    "flagged": false,
    "reason": null,
    "severity": "safe"
  },
  "timestamp": "2026-01-28T20:30:00",
  "saved_to_db": true
}
```

#### GET /api/v1/sentiment/history?limit=10

Retrieve recent sentiment analyses.

**Parameters:**

- `limit` (optional): Number of records to return (1-100), default: 10

#### POST /api/v1/sentiment/feedback/{analysis_id}

Submit user feedback (thumbs up/down) for an analysis.

```bash
curl -X POST "https://sentiment-dashboard-api.onrender.com/api/v1/sentiment/feedback/123?feedback=positive"
```

---

## 📁 Project Structure

```
sentiment-dashboard/
├── setup.sh                      # One-command setup for Mac/Linux
├── setup.ps1                     # One-command setup for Windows
├── .env.example                  # Environment variable template
├── docker-compose.yml            # Docker setup (PostgreSQL + backend + frontend)
│
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   │   └── sentiment.py      # Sentiment analysis routes
│   │   ├── core/                 # Core configuration
│   │   │   └── config.py         # App settings
│   │   ├── models/               # Data models
│   │   │   └── schemas.py        # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   │   ├── sentiment_analyzer.py    # VADER analyzer
│   │   │   ├── distilbert_analyzer.py   # Hybrid model
│   │   │   └── content_moderator.py     # Content filtering
│   │   ├── database.py           # PostgreSQL connection
│   │   └── main.py               # FastAPI app entry point
│   ├── tests/                    # Test suite (53 tests)
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Local environment variables (git ignored)
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   └── BatchUpload.jsx   # CSV batch upload
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.jsx               # Main component
│   │   ├── App.css               # Styling
│   │   └── main.jsx              # Entry point
│   ├── package.json
│   └── .env                      # API URL config (git ignored)
│
└── README.md
```

---

## 🧪 Testing

### Running Tests

```bash
cd backend

# Mac/Linux
source venv/bin/activate
# Windows
# .\venv\Scripts\Activate.ps1

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term

# View HTML coverage report
# Mac/Linux:
open htmlcov/index.html
# Windows:
Start-Process .\htmlcov\index.html
```

### Test Coverage

**Overall Coverage: 79.34%** (53 tests, 426 statements)

| Component              | Coverage | Status |
| ---------------------- | -------- | ------ |
| schemas.py             | 100%     | ✅     |
| sentiment_analyzer.py  | 94.44%   | ✅     |
| config.py              | 92.31%   | ✅     |
| content_moderator.py   | 90.91%   | ✅     |
| distilbert_analyzer.py | 81.16%   | ✅     |
| main.py                | 70.00%   | ✅     |
| database.py            | 65.00%   | ✅     |

### Test Suite Breakdown

- **Sentiment Analyzer Tests** (10 tests) - positive/negative/neutral classification, negation handling, model selection
- **API Endpoint Tests** (17 tests) - all endpoints, request validation, response structure
- **Hybrid Analyzer Tests** (10 tests) - sarcasm, slang, negations, edge cases
- **Database Tests** (8 tests) - connection management, CRUD, cleanup, error handling
- **Content Moderator Tests** (4 tests) - safe content, harmful patterns, severity levels
- **Main Application Tests** (4 tests) - root endpoint, health check, CORS, docs

### Test the Live App

Visit: https://sentiment-dashboard-zeta.vercel.app/

```
Negation:  "This is not bad at all"  → Fast: 😞 Negative | Precise: 😊 Positive ✅
Slang:     "This movie slaps!"       → Fast: 😞 Negative | Precise: 😊 Positive ✅
Irony:     "Thanks for nothing"      → Fast: 😊 Positive | Precise: 😞 Negative ✅
```

### Test the API

```bash
# Fast Mode
curl -X POST "https://sentiment-dashboard-api.onrender.com/api/v1/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is not bad!", "model": "vader"}'

# Precise Mode
curl -X POST "https://sentiment-dashboard-api.onrender.com/api/v1/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is not bad!", "model": "distilbert"}'
```

---

## 🌟 Key Technical Achievements

**1. Hybrid Model Architecture** — Combined VADER + TextBlob with custom pattern boosting for 10-15% accuracy improvement while staying under 10MB memory.

**2. Resource Optimization** — Engineered to run within Render's 512MB free tier RAM constraint through lazy loading and efficient query design.

**3. Pattern Recognition System** — Custom regex-based system handling negations, modern slang, and irony detection that traditional models miss.

**4. Production Deployment** — Zero-downtime deployments via GitHub integration on both Vercel (frontend) and Render (backend).

**5. Content Safety** — Comprehensive harmful content detection with 41+ patterns, real-time severity classification, and automatic censoring.

**6. Batch Processing** — Client-side CSV parsing handles up to 1,000 rows with real-time progress tracking, optimized for free-tier constraints.

**7. Comprehensive Testing** — 53 passing tests with 79.34% coverage, including edge cases for sarcasm, slang, and negation. Full suite runs in under 1 second.

**8. Cross-Platform Developer Experience** — One-command setup scripts for Mac, Linux, and Windows reduce onboarding time from 30 minutes to under 5 minutes.

---

## 📚 Learning Outcomes

- ✅ **Full-stack development** (React + FastAPI)
- ✅ **RESTful API design** and implementation
- ✅ **Cloud deployment** (Vercel + Render)
- ✅ **Database integration** (PostgreSQL)
- ✅ **AI/ML integration** (VADER + TextBlob)
- ✅ **Hybrid model architecture** (multi-model combining)
- ✅ **Pattern recognition** (regex-based boosting)
- ✅ **Performance optimization** (memory-constrained environments)
- ✅ **Content moderation** (safety and filtering)
- ✅ **Modern JavaScript** (React Hooks, async/await)
- ✅ **Python async programming** (FastAPI)
- ✅ **Environment variable management**
- ✅ **Git version control** with feature branches
- ✅ **CSV processing** (batch file uploads)
- ✅ **Unit & integration testing** (pytest, fixtures, mocking)
- ✅ **Code coverage analysis** (pytest-cov, HTML reports)
- ✅ **Edge case handling** (negations, sarcasm, empty inputs)
- ✅ **Developer experience** (cross-platform setup automation)

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
- [x] Analytics dashboard with Recharts (pie, timeline, distribution charts)
- [x] User feedback system (thumbs up/down)
- [x] Model tracking with visual badges (⚡ Fast / 🎯 Precise)

### Phase 3: Professional Polish 🚧 In Progress

- [x] Comprehensive test suite (53 tests, 79% coverage)
- [x] Cross-platform setup scripts (Mac/Linux/Windows)
- [ ] **OpenAI GPT-4o-mini integration** — emotion detection, AI reasoning explanations
- [ ] **CI/CD Pipeline** — GitHub Actions for automated testing on every push
- [ ] **Redis caching** — reduce API costs by 80% through request deduplication
- [ ] **JWT Authentication** — secure API endpoints with user accounts
- [ ] **WebSockets** — real-time live sentiment updates

---

## 🚀 Performance Note

This application is optimized for free-tier hosting (512MB RAM) with <100ms response times. The backend may take 30-60 seconds to wake on first request after 15 minutes of inactivity (Render free tier cold start), but subsequent requests are instant.

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
- **FastAPI** - Sebastián Ramírez
- **React** - Meta/Facebook
- **Papaparse** - Matt Holt
- **Vercel & Render** - Deployment platforms

---

**⭐ Star this repo if you find it useful!**
