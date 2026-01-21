#!/bin/bash

echo "🚀 Setting up Sentiment Dashboard..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python and Node.js are installed"
echo ""

# Backend setup
echo "${BLUE}Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your API keys"
fi

cd ..

# Frontend setup
echo ""
echo "${BLUE}Setting up Frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

cd ..

echo ""
echo "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your Reddit API credentials"
echo "2. Start MongoDB: docker run -d -p 27017:27017 mongo:7.0"
echo "3. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "4. Start frontend: cd frontend && npm run dev"
echo "5. Open http://localhost:3000"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"
echo ""
echo "See SETUP_GUIDE.md for detailed instructions"
