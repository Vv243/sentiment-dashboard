#!/bin/bash
# ===========================================
# Sentiment Analysis Dashboard - Mac/Linux Setup
# ===========================================
# Usage: chmod +x setup.sh && ./setup.sh

set -e

echo ""
echo "🚀 Sentiment Analysis Dashboard - Setup"
echo "========================================"

# ---- Check Prerequisites ----
echo ""
echo "📋 Checking prerequisites..."

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        echo "   $2"
        exit 1
    else
        echo "✅ $1 found: $($1 --version 2>&1 | head -n 1)"
    fi
}

check_command python3 "https://www.python.org/downloads/"
check_command node "https://nodejs.org/"
check_command git "https://git-scm.com/"
check_command psql "brew install postgresql@14 (Mac) or apt install postgresql (Linux)"

# ---- Start PostgreSQL ----
echo ""
echo "🗄️  Starting PostgreSQL..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew services start postgresql@14 2>/dev/null || brew services start postgresql 2>/dev/null || true
else
    sudo service postgresql start 2>/dev/null || sudo systemctl start postgresql 2>/dev/null || true
fi
sleep 2

# ---- Create Database ----
echo ""
echo "🗄️  Creating local database..."
createdb sentiment_local 2>/dev/null && echo "✅ Database 'sentiment_local' created" || echo "✅ Database 'sentiment_local' already exists"

# ---- Backend Setup ----
echo ""
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

source venv/bin/activate
pip install -r requirements.txt -q
echo "✅ Python dependencies installed"

if [ ! -f ".env" ]; then
    USERNAME=$(whoami)
    echo "DATABASE_URL=postgresql://$USERNAME@localhost/sentiment_local" > .env
    echo "✅ Created backend/.env with your username ($USERNAME)"
else
    echo "✅ backend/.env already exists"
fi

cd ..

# ---- Frontend Setup ----
echo ""
echo "⚛️  Setting up frontend..."
cd frontend
npm install -q
echo "✅ Node dependencies installed"

if [ ! -f ".env" ]; then
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo "✅ Created frontend/.env"
else
    echo "✅ frontend/.env already exists"
fi
cd ..

# ---- Done ----
echo ""
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "To start the project, open 2 terminal tabs:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python -m uvicorn app.main:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "  Then open: http://localhost:3000"
echo "========================================"
