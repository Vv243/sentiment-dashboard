# Setup Guide - Sentiment Dashboard

This guide will help you get the Sentiment Analysis Dashboard up and running on your local machine.

## 📋 Prerequisites

Make sure you have the following installed:
- Python 3.9 or higher
- Node.js 16 or higher
- MongoDB (or Docker)
- Git

## 🚀 Quick Start (Recommended)

### Option 1: Using Docker (Easiest)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd sentiment-dashboard
```

2. **Set up environment variables**
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and add your API keys

# Frontend
cd ../frontend
cp .env.example .env
```

3. **Start all services**
```bash
cd ..
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Step 1: Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see below)

# Start backend server
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

#### Step 2: Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

#### Step 3: Set Up MongoDB

**Option A: Using Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

**Option B: Local Installation**
- macOS: `brew install mongodb-community`
- Ubuntu: Follow [MongoDB installation guide](https://docs.mongodb.com/manual/installation/)
- Windows: Download from [MongoDB website](https://www.mongodb.com/try/download/community)

## 🔑 Getting API Keys

### Reddit API (Recommended for getting started)

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - Name: "Sentiment Analyzer"
   - App type: Select "script"
   - Description: "Sentiment analysis project"
   - Redirect URI: http://localhost:8000
4. Click "Create app"
5. Copy:
   - Client ID (under app name)
   - Client Secret
6. Add to `.env`:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=sentiment_analyzer_v1.0
```

### Twitter API (Optional)

Twitter API is more restrictive. For free tier:

1. Go to https://developer.twitter.com/
2. Apply for a developer account
3. Create a new project and app
4. Get your Bearer Token
5. Add to `.env`:
```
TWITTER_BEARER_TOKEN=your_bearer_token
```

**Note**: Twitter's free tier has limited functionality. Reddit is recommended for this project.

## 🧪 Testing the Application

### 1. Test Backend API

```bash
# Check health
curl http://localhost:8000/health

# Analyze sample text
curl -X POST http://localhost:8000/api/v1/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Tesla stock is going to the moon! 🚀", "use_vader": true}'
```

### 2. Collect Data

```bash
# Collect data for TSLA
curl -X POST "http://localhost:8000/api/v1/collection/collect-now/TSLA?source=reddit"

# Check sentiment
curl http://localhost:8000/api/v1/sentiment/TSLA

# Get historical data
curl "http://localhost:8000/api/v1/sentiment/TSLA/history?days=7"
```

### 3. Test Frontend

1. Open http://localhost:3000
2. Search for a ticker (e.g., TSLA, AAPL)
3. Click "Refresh Data" to collect new data
4. View sentiment gauge and historical chart

## 📊 Using the Dashboard

### Collecting Data

1. **Search for a ticker**: Enter any stock symbol (TSLA, AAPL, GME, etc.)
2. **Collect data**: Click the "Refresh Data" button
3. **Wait for analysis**: The system will:
   - Fetch posts from Reddit
   - Analyze sentiment using VADER
   - Store results in MongoDB
   - Display visualizations

### Understanding the Results

**Sentiment Score (-1 to 1)**
- **Positive** (>0.05): 😊 Generally bullish sentiment
- **Neutral** (-0.05 to 0.05): 😐 Mixed or neutral sentiment
- **Negative** (<-0.05): 😟 Generally bearish sentiment

**Components**
- Positive %: Proportion of positive sentiment
- Negative %: Proportion of negative sentiment
- Neutral %: Proportion of neutral sentiment

## 🔧 Troubleshooting

### Backend Issues

**Problem: Can't connect to MongoDB**
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Or for local installation
systemctl status mongod  # Linux
brew services list | grep mongodb  # macOS
```

**Problem: Import errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Reddit API errors**
- Verify your credentials in `.env`
- Check Reddit is accessible in your region
- Ensure you're not rate-limited (wait a few minutes)

### Frontend Issues

**Problem: Can't connect to backend**
- Check backend is running on port 8000
- Verify `VITE_API_URL` in frontend `.env`

**Problem: npm install fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Data Collection Issues

**Problem: No data for ticker**
- Try popular tickers first (TSLA, AAPL, GME)
- Reddit might not have recent posts for obscure stocks
- Try different subreddits in the code (wallstreetbets, stocks, investing)

**Problem: Slow data collection**
- Normal for first time (downloading VADER model)
- Reddit API can be slow
- Collection is asynchronous - refresh after 30 seconds

## 📈 Next Steps

1. **Add more tickers**: Test with different stock symbols
2. **Adjust time ranges**: Modify historical data timeframes
3. **Customize subreddits**: Edit `reddit_collector.py` to target specific communities
4. **Enable FinBERT**: Set `USE_FINBERT=True` in `.env` for financial-specific sentiment (requires more RAM/GPU)
5. **Deploy to production**: See deployment guide in README.md

## 🆘 Getting Help

- Check API documentation: http://localhost:8000/docs
- Review logs:
  ```bash
  # Backend logs
  docker-compose logs backend
  
  # MongoDB logs
  docker-compose logs mongodb
  ```
- Common issues are usually:
  - Missing environment variables
  - MongoDB not running
  - Invalid API credentials

## 🎯 Testing Checklist

- [ ] Backend server starts successfully
- [ ] Frontend loads without errors
- [ ] MongoDB connection is established
- [ ] Can analyze sample text via API
- [ ] Can collect data for a ticker
- [ ] Sentiment data displays correctly
- [ ] Historical chart renders
- [ ] Trending topics appear (after collecting multiple tickers)

Happy analyzing! 🚀
