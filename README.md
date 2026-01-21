# Real-Time Sentiment Analysis Dashboard

A full-stack application that performs real-time sentiment analysis on social media data (Twitter/Reddit) for stocks and cryptocurrencies, with live visualization dashboard.

## 🎯 Features

- **Real-time Data Collection**: Automated fetching from Twitter/Reddit APIs
- **Sentiment Analysis**: VADER + FinBERT dual sentiment scoring
- **Intelligent Fallback System**: Automatic synthetic data generation when APIs unavailable
- **Live Dashboard**: React-based UI with real-time updates
- **Historical Trends**: Track sentiment over time with interactive charts
- **Multi-Asset Support**: Compare sentiment across multiple stocks/crypto
- **REST API**: Clean, documented API endpoints
- **Market Scenarios**: Generate demo data for bullish/bearish/volatile conditions

## 🏗️ Architecture

```
sentiment-dashboard/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Config, security
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── tests/
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API calls
│   │   ├── hooks/         # Custom hooks
│   │   └── utils/         # Helper functions
│   └── package.json
└── docker-compose.yml     # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (or Docker)
- Twitter API credentials OR Reddit API credentials

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run migrations (if using SQL)
# alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend runs on http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install

# Create .env file
cp .env.example .env
# Edit with backend URL

# Start development server
npm start
```

Frontend runs on http://localhost:3000

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 API Endpoints

### Sentiment Analysis
- `POST /api/v1/analyze` - Analyze text sentiment
- `GET /api/v1/sentiment/{ticker}` - Get latest sentiment for ticker
- `GET /api/v1/sentiment/{ticker}/history` - Get historical sentiment data

### Data Collection
- `POST /api/v1/collect/start` - Start data collection for ticker
- `POST /api/v1/collect/stop` - Stop data collection
- `POST /api/v1/collection/collect-now/{ticker}` - Immediate collection with auto-fallback
- `POST /api/v1/collection/generate-demo-data/{ticker}` - Generate synthetic demo data
- `GET /api/v1/trending` - Get trending topics

### Health
- `GET /health` - Health check
- `GET /metrics` - API metrics

**📖 Full API Documentation**: http://localhost:8000/docs

## 🔄 Backup System

The application includes an **intelligent fallback system** for when social media APIs are unavailable:

**Automatic Fallback**: Reddit → Twitter → Synthetic Data

- No API credentials needed to start developing
- Works for demos/interviews even if APIs are down
- Generate realistic synthetic data for testing
- Create specific market scenarios (bullish/bearish/volatile)

**📖 See [BACKUP_PLAN.md](BACKUP_PLAN.md) for full documentation**

**Quick demo data generation:**
```bash
curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/TSLA?scenario=bullish"
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sentiment_db

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Twitter API (Option 1)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_secret

# Reddit API (Option 2)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=sentiment_analyzer

# Sentiment Models
USE_VADER=True
USE_FINBERT=True
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Backend (Render/Railway)
1. Create new web service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Frontend (Vercel/Netlify)
1. Connect GitHub repo
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Add environment variables

## 🎨 Tech Stack

**Backend**
- FastAPI - Web framework
- MongoDB - Database
- Redis - Caching & message broker
- Celery - Background tasks
- VADER - Sentiment analysis
- Transformers (FinBERT) - Financial sentiment
- PRAW/Tweepy - Social media APIs

**Frontend**
- React - UI framework
- Recharts - Data visualization
- Axios - HTTP client
- TanStack Query - Data fetching
- Tailwind CSS - Styling
- Socket.io-client - Real-time updates

## 📈 Development Roadmap

- [x] Project setup
- [ ] Week 1: Backend + Data Pipeline
  - [ ] FastAPI setup with basic endpoints
  - [ ] MongoDB integration
  - [ ] Twitter/Reddit API integration
  - [ ] VADER sentiment analysis
  - [ ] Background task scheduling
- [ ] Week 2: Frontend + Deployment
  - [ ] React dashboard with charts
  - [ ] Real-time updates
  - [ ] Multi-ticker comparison
  - [ ] Responsive design
  - [ ] Deploy to production

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

## 📝 License

MIT License - feel free to use this for your own portfolio

## 👤 Author

Vinh Pham
- LinkedIn: [linkedin.com/in/vinhpham243](https://linkedin.com/in/vinhpham243)
- Email: vietvinh2432001@gmail.com

---

**Note**: This project demonstrates skills in full-stack development, real-time data processing, machine learning deployment, and modern DevOps practices.
