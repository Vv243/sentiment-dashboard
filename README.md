# Sentiment Analysis Dashboard

A real-time sentiment analysis platform that analyzes social media sentiment for stocks and cryptocurrencies.

## Features

- Real-time sentiment analysis using VADER
- RESTful API built with FastAPI
- Social media data collection (Reddit/Twitter)
- Interactive dashboard with React
- Docker containerization
- MongoDB database

## Tech Stack

**Backend:**
- FastAPI
- Python 3.13
- MongoDB
- VADER Sentiment Analysis
- PRAW (Reddit API)

**Frontend:**
- React
- Vite
- Recharts
- Tailwind CSS

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB

### Backend Setup

\\\ash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-fixed.txt
cp .env.example .env
uvicorn app.main:app --reload
\\\

Backend runs on http://localhost:8000

### Frontend Setup

\\\ash
cd frontend
npm install
npm run dev
\\\

Frontend runs on http://localhost:3000

## API Documentation

Interactive API docs available at: http://localhost:8000/docs

## Usage

1. Start the backend server
2. Start the frontend development server
3. Navigate to http://localhost:3000
4. Search for a stock ticker (e.g., TSLA, AAPL)
5. View real-time sentiment analysis

## Project Structure

\\\
sentiment-dashboard/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── models/   # Data models
│   │   └── services/ # Business logic
│   └── requirements-fixed.txt
└── frontend/          # React frontend
    └── src/
        ├── components/
        └── services/
\\\

## Development Status

- [x] FastAPI backend setup
- [x] Basic API endpoints
- [x] Sentiment analysis integration
- [ ] Database integration
- [ ] Frontend implementation
- [ ] Deployment

## License

MIT
