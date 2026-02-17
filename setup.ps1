# ===========================================
# Sentiment Analysis Dashboard - Windows Setup
# ===========================================
# Usage: Right-click PowerShell > Run as Administrator, then:
#   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
#   .\setup.ps1

Write-Host ""
Write-Host "🚀 Sentiment Analysis Dashboard - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

function Check-Command($cmd, $installUrl) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $version = & $cmd --version 2>&1 | Select-Object -First 1
        Write-Host "✅ $cmd found: $version" -ForegroundColor Green
    } else {
        Write-Host "❌ $cmd is not installed. Install from: $installUrl" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
Check-Command "python" "https://www.python.org/downloads/"
Check-Command "node" "https://nodejs.org/"
Check-Command "git" "https://git-scm.com/"
Check-Command "psql" "https://www.postgresql.org/download/windows/"

Write-Host ""
Write-Host "🗄️  Creating local database..." -ForegroundColor Yellow
$dbExists = & psql -U postgres -lqt 2>&1 | Select-String "sentiment_local"
if ($dbExists) {
    Write-Host "✅ Database 'sentiment_local' already exists" -ForegroundColor Green
} else {
    & createdb -U postgres sentiment_local
    Write-Host "✅ Database 'sentiment_local' created" -ForegroundColor Green
}

Write-Host ""
Write-Host "🐍 Setting up backend..." -ForegroundColor Yellow
Set-Location backend

if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

if (-Not (Test-Path ".env")) {
    "DATABASE_URL=postgresql://postgres@localhost/sentiment_local" | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "✅ Created backend/.env" -ForegroundColor Green
} else {
    Write-Host "✅ backend/.env already exists" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "⚛️  Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend
npm install -q
Write-Host "✅ Node dependencies installed" -ForegroundColor Green

if (-Not (Test-Path ".env")) {
    "VITE_API_URL=http://localhost:8000" | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "✅ Created frontend/.env" -ForegroundColor Green
} else {
    Write-Host "✅ frontend/.env already exists" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Terminal 1 (Backend):" -ForegroundColor Yellow
Write-Host "    cd backend"
Write-Host "    .\venv\Scripts\Activate.ps1"
Write-Host "    python -m uvicorn app.main:app --reload"
Write-Host ""
Write-Host "  Terminal 2 (Frontend):" -ForegroundColor Yellow
Write-Host "    cd frontend"
Write-Host "    npm run dev"
Write-Host ""
Write-Host "  Then open: http://localhost:3000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
