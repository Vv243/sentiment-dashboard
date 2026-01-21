# Git Quick Start - Visual Guide

## 🚀 Upload Your Project in 5 Minutes

### Step 1: Install Git ⬇️

**Windows**: https://git-scm.com/download/win
**Mac**: `brew install git`
**Linux**: `sudo apt install git`

Verify:
```bash
git --version
```

---

### Step 2: Configure Git (Once) ⚙️

```bash
git config --global user.name "Vinh Pham"
git config --global user.email "vietvinh2432001@gmail.com"
```

---

### Step 3: Initialize Your Project 📁

```bash
cd sentiment-dashboard
git init
git add .
git commit -m "Initial commit - Sentiment Dashboard"
```

**What This Does:**
- `git init` - Start tracking this folder
- `git add .` - Stage all files
- `git commit` - Save a snapshot

---

### Step 4: Create GitHub Repository 🌐

1. Go to: **https://github.com**
2. Login/Sign up
3. Click **"+"** (top-right) → **"New repository"**
4. Fill in:
   ```
   Repository name: sentiment-dashboard
   Description: Real-time sentiment analysis dashboard
   Public ✓
   ```
5. Click **"Create repository"**

❌ **DO NOT** check "Add a README" - we have one!

---

### Step 5: Connect & Push 🚀

Copy your GitHub username, then run:

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/sentiment-dashboard.git
git branch -M main
git push -u origin main
```

**Enter your GitHub password when asked.**

✅ **Done!** Visit: `https://github.com/YOUR_USERNAME/sentiment-dashboard`

---

## 🔄 Daily Workflow (After Initial Setup)

### Making Changes:

```
┌─────────────────────────────────────────┐
│  1. Edit code in VS Code                │
│     (Make your changes)                 │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  2. git status                          │
│     (See what changed)                  │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  3. git add .                           │
│     (Stage all changes)                 │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  4. git commit -m "Description"         │
│     (Save snapshot)                     │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  5. git push                            │
│     (Upload to GitHub)                  │
└─────────────────────────────────────────┘
```

---

## 📋 Essential Commands

| Command | What It Does |
|---------|-------------|
| `git status` | Check what changed |
| `git add .` | Stage all changes |
| `git add filename` | Stage specific file |
| `git commit -m "msg"` | Save a snapshot |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| `git log` | See history |

---

## 🎯 Real Example

You just added the backup system:

```bash
# 1. Check status
git status
# Output: modified: backend/app/api/collection.py
#         new file: backend/app/services/synthetic_data.py

# 2. Stage changes
git add .

# 3. Commit
git commit -m "Add synthetic data fallback system"

# 4. Push to GitHub
git push

# ✅ Done! Changes are live on GitHub
```

---

## 🌿 Using Branches (Optional)

For working on new features without breaking main code:

```bash
# Create new branch
git checkout -b feature/new-dashboard

# Make changes...
git add .
git commit -m "Redesign dashboard"

# Push branch
git push -u origin feature/new-dashboard

# Later: merge back to main
git checkout main
git merge feature/new-dashboard
git push
```

---

## 🎨 GitHub Profile Tips

### 1. Pin Your Best Projects

Your profile → "Customize pins" → Select sentiment-dashboard

### 2. Add Topics

Repository page → ⚙️ (next to About) → Add:
- `python`
- `react`
- `machine-learning`
- `sentiment-analysis`
- `fastapi`

### 3. Add Profile README

Create special repo: `YOUR_USERNAME/YOUR_USERNAME`

```markdown
# Hi, I'm Vinh! 👋

🎓 CS Student @ Rutgers
💼 Seeking AI/ML roles
🚀 Check out my Sentiment Dashboard!

[GitHub](https://github.com/YOUR_USERNAME) | 
[LinkedIn](https://linkedin.com/in/vinhpham243)
```

---

## 🔧 VS Code Git Integration

### Visual Git in VS Code:

1. Click **Source Control** icon (left sidebar) or `Ctrl+Shift+G`
2. See all changed files
3. Click **"+"** to stage
4. Type commit message
5. Click **✓** to commit
6. Click **"..."** → **"Push"**

**No terminal needed!** 🎉

---

## ⚠️ Important: .gitignore

**Never commit these:**

```gitignore
# Already in your .gitignore!
.env
venv/
node_modules/
__pycache__/
*.pyc
```

If you accidentally committed `.env`:

```bash
git rm --cached backend/.env
git commit -m "Remove .env"
git push
```

Then **change your API keys immediately!**

---

## 🆘 Common Problems

### Problem: "Permission denied"

**Solution**: Use HTTPS URL
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/sentiment-dashboard.git
```

### Problem: "Failed to push"

**Solution**: Pull first
```bash
git pull --rebase
git push
```

### Problem: "Not a git repository"

**Solution**: Run in project folder
```bash
cd sentiment-dashboard
git init
```

### Problem: Made a mistake in commit

**Solution**: Undo last commit
```bash
git reset --soft HEAD~1
# Edit files
git add .
git commit -m "Correct message"
```

---

## ✅ Checklist Before Sharing

- [ ] `.env` file is in `.gitignore`
- [ ] README.md is informative
- [ ] Code has comments
- [ ] Repository is public
- [ ] Added description and topics on GitHub
- [ ] Tested by cloning in new folder
- [ ] No sensitive data committed

---

## 🎬 Video Tutorials

**Learn Git Visually:**
- Git Explained in 100 Seconds: https://www.youtube.com/watch?v=hwP7WQkmECE
- Git Tutorial for Beginners: https://www.youtube.com/watch?v=8JJ101D3knE

**GitHub Guides:**
- Hello World: https://guides.github.com/activities/hello-world/

---

## 📊 Git Workflow Diagram

```
Working Directory          Staging Area           Repository (Local)      GitHub (Remote)
┌─────────────┐           ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│             │           │             │        │             │        │             │
│  Your Code  │ git add   │   Staged    │ commit │   Commits   │  push  │   GitHub    │
│   (Edit)    │ ────────► │   Changes   │────────►│  (History)  │────────►│  Repository │
│             │           │             │        │             │        │             │
└─────────────┘           └─────────────┘        └─────────────┘        └─────────────┘
                                                         │                       │
                                                         │ pull                  │
                                                         └───────────────────────┘
```

---

## 💡 Pro Tips

1. **Commit often** - Small, focused commits
2. **Write clear messages** - "Add feature" not "update"
3. **Pull before push** - Avoid conflicts
4. **Use branches** - Keep main stable
5. **Read the status** - `git status` is your friend

---

## 🏆 After Upload

### Add to Resume:

```
PROJECTS

Sentiment Analysis Dashboard                    github.com/YOUR_USERNAME/sentiment-dashboard
• Real-time stock sentiment analysis using Reddit API and VADER
• Technologies: Python, FastAPI, React, MongoDB, Docker
```

### Share on LinkedIn:

```
🚀 Just launched my Sentiment Dashboard project!

A full-stack app analyzing social media sentiment for stocks:
✓ FastAPI backend with RESTful API
✓ React dashboard with live charts
✓ Intelligent fallback system
✓ Docker containerization

Check it out: github.com/YOUR_USERNAME/sentiment-dashboard

#Python #React #MachineLearning #OpenToWork
```

---

## 🎯 Your Action Plan

**Today:**
- [ ] Install Git
- [ ] Configure name & email
- [ ] `git init` in your project
- [ ] First commit
- [ ] Create GitHub repository
- [ ] Push to GitHub

**This Week:**
- [ ] Make regular commits as you code
- [ ] Add good README
- [ ] Add topics to repo
- [ ] Pin repo on profile

**For Job Applications:**
- [ ] Add GitHub link to resume
- [ ] Share projects on LinkedIn
- [ ] Keep repository updated

---

**Ready? Let's do this!** 🚀

Start with Step 1: Install Git!
