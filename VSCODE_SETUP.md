# VS Code Setup Guide - Step by Step

Follow these steps exactly to set up your Sentiment Dashboard project in VS Code.

## ✅ Prerequisites Checklist

Before starting, ensure you have:
- [ ] VS Code installed (latest version)
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] Git installed (`git --version`)
- [ ] Docker installed (optional but recommended)

---

## 📁 Step 1: Open Project in VS Code

```bash
# Navigate to the project
cd sentiment-dashboard

# Open in VS Code
code .
```

**Alternative:** Open VS Code → File → Open Folder → Select `sentiment-dashboard`

---

## 🔌 Step 2: Install Extensions

When you open the project, VS Code should show a popup: **"This workspace has extension recommendations"**

Click **"Install All"** to install all recommended extensions.

**If popup doesn't appear:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: "Show Recommended Extensions"
3. Install each extension manually

**Must-have extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- Python Debugger (Microsoft)
- ES7+ React/Redux snippets
- Tailwind CSS IntelliSense
- Prettier
- Docker
- Thunder Client

After installing, **reload VS Code** when prompted.

---

## 🐍 Step 3: Set Up Python Backend

### 3.1 Open Integrated Terminal

Press `` Ctrl+` `` (backtick) to open the terminal in VS Code.

### 3.2 Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 3.3 Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### 3.4 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 2-3 minutes. You should see packages installing.

### 3.5 Select Python Interpreter in VS Code

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P`)
2. Type: "Python: Select Interpreter"
3. Choose: `./backend/venv/bin/python` (or `.\backend\venv\Scripts\python.exe` on Windows)

You should now see "Python 3.x.x ('venv')" in the bottom-left status bar.

### 3.6 Create Environment File

```bash
# Still in backend directory
cp .env.example .env
```

Now edit `.env` file - we'll do this in Step 5.

---

## ⚛️ Step 4: Set Up React Frontend

### 4.1 Open New Terminal

Click the **"+"** button in the terminal panel to open a new terminal (or split terminal).

### 4.2 Install Node Dependencies

```bash
cd frontend
npm install
```

This will take 1-2 minutes.

### 4.3 Create Environment File

```bash
cp .env.example .env
```

The default values in `.env` should work for local development.

---

## 🔑 Step 5: Get API Keys

### Reddit API (Recommended - Free and Easy)

1. Go to: https://www.reddit.com/prefs/apps
2. Click **"Create App"** or **"Create Another App"**
3. Fill in:
   - **name**: "Sentiment Analyzer"
   - **App type**: Select "script"
   - **description**: "Sentiment analysis for school project"
   - **redirect uri**: http://localhost:8000
4. Click **"Create app"**
5. Copy the credentials:
   - **Client ID**: The string under your app name (looks like: `abc123XYZ`)
   - **Client Secret**: Click "secret" to reveal it

### Add to Backend .env File

1. In VS Code, open `backend/.env`
2. Update these lines:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=sentiment_analyzer_v1.0
```

**Save the file** (`Ctrl+S` or `Cmd+S`)

---

## 🗄️ Step 6: Start MongoDB

You have 2 options:

### Option A: Using Docker (Recommended)

```bash
docker run -d -p 27017:27017 --name sentiment_mongodb mongo:7.0
```

To verify it's running:
```bash
docker ps
```

You should see `sentiment_mongodb` in the list.

### Option B: Local MongoDB Installation

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**Ubuntu/Debian:**
```bash
# Follow: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
```

**Windows:**
Download from: https://www.mongodb.com/try/download/community

---

## 🚀 Step 7: Run the Application

### Method 1: Using VS Code Terminal (Recommended for Development)

You'll need **3 terminal windows**. In VS Code:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Monitoring/Commands:**
Keep this free for running commands.

### Method 2: Using VS Code Tasks

1. Press `Ctrl+Shift+P`
2. Type: "Tasks: Run Task"
3. Select: "Start All Services (Docker)"

### Method 3: Using Debugger

1. Go to **Run and Debug** panel (`Ctrl+Shift+D`)
2. Select **"Python: FastAPI Backend"** from dropdown
3. Click green play button (or press `F5`)
4. Set breakpoints by clicking left of line numbers

---

## ✅ Step 8: Verify Everything Works

### 8.1 Check Backend

Open browser: http://localhost:8000/docs

You should see FastAPI's Swagger documentation.

### 8.2 Check Frontend

Open browser: http://localhost:3000

You should see the Sentiment Dashboard.

### 8.3 Test API in VS Code

1. Install **Thunder Client** extension if not already installed
2. Click Thunder Client icon in left sidebar
3. Create new request:
   - **Method**: POST
   - **URL**: http://localhost:8000/api/v1/sentiment/analyze
   - **Body** (JSON):
   ```json
   {
     "text": "Tesla stock is amazing! 🚀",
     "use_vader": true
   }
   ```
4. Click **Send**

You should get a response with sentiment scores.

---

## 🧪 Step 9: Test Data Collection

### In Terminal:

```bash
curl -X POST "http://localhost:8000/api/v1/collection/collect-now/TSLA?source=reddit"
```

### Or use Thunder Client:

- **Method**: POST
- **URL**: http://localhost:8000/api/v1/collection/collect-now/TSLA?source=reddit
- Click **Send**

Wait 10-20 seconds, then check:

```bash
curl http://localhost:8000/api/v1/sentiment/TSLA
```

You should see sentiment data for TSLA!

### In the Frontend:

1. Go to http://localhost:3000
2. Search for "TSLA"
3. Click **"Refresh Data"**
4. Wait 10-20 seconds
5. You should see sentiment gauge, chart, and stats!

---

## 🎨 Step 10: VS Code Workspace Organization

### Recommended Layout:

1. **Left Sidebar**: Explorer view with files
2. **Center**: Code editor (split vertically if needed)
3. **Bottom**: Terminal panel with 3 terminals
4. **Right** (optional): Outline/Extensions panel

### Useful Shortcuts:

- `Ctrl+B` - Toggle sidebar
- `Ctrl+J` - Toggle terminal
- `` Ctrl+` `` - Focus terminal
- `Ctrl+\` - Split editor
- `Ctrl+P` - Quick file open
- `Ctrl+Shift+F` - Search in files
- `F5` - Start debugging
- `Ctrl+Shift+D` - Open debug panel

---

## 🔧 Troubleshooting

### "Python interpreter not found"
1. `Ctrl+Shift+P`
2. "Python: Select Interpreter"
3. Choose `./backend/venv/bin/python`

### "Module not found" errors
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### MongoDB connection failed
```bash
# Check if MongoDB is running
docker ps | grep mongo

# If not, start it
docker run -d -p 27017:27017 --name sentiment_mongodb mongo:7.0
```

### Frontend not starting
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Port already in use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## 🎯 Next Steps

Now that everything is set up:

1. ✅ Explore the codebase
2. ✅ Read `PROJECT_PLAN.md` for implementation guide
3. ✅ Try collecting data for different tickers
4. ✅ Modify the UI and see changes live
5. ✅ Add your own features
6. ✅ Deploy to production (follow README.md)

---

## 💡 Pro Tips

1. **Use Git Early**: Initialize git and commit often
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Use Breakpoints**: Click left of line numbers to set breakpoints, then press F5

3. **Format on Save**: Already configured! Just press `Ctrl+S`

4. **Multi-cursor**: `Alt+Click` to add cursors, edit multiple lines at once

5. **Command Palette**: `Ctrl+Shift+P` is your best friend - search any command

6. **Integrated Git**: Use Source Control panel (`Ctrl+Shift+G`) for git operations

---

## ✅ Final Checklist

Before you start coding:
- [ ] VS Code opens the project
- [ ] All extensions installed
- [ ] Backend virtual environment activated
- [ ] Frontend npm packages installed
- [ ] MongoDB running
- [ ] Backend accessible at localhost:8000
- [ ] Frontend accessible at localhost:3000
- [ ] Reddit API keys configured
- [ ] Can collect data for a ticker
- [ ] Tests pass (`pytest tests/`)

If all checked, **you're ready to build!** 🚀

---

Happy coding! If you run into issues, check the main SETUP_GUIDE.md or the troubleshooting section above.
