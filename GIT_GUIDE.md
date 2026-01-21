# Git & GitHub Guide - Complete Beginner to Upload

## 🎯 What is Git & GitHub?

- **Git**: Version control system (tracks changes to your code)
- **GitHub**: Website where you store your Git projects online

Think of it like:
- Git = Saving your game progress
- GitHub = Cloud save that others can see

---

## 📋 Prerequisites

### 1. Install Git

**Windows:**
- Download: https://git-scm.com/download/win
- Run installer (use default settings)
- Verify: Open Command Prompt and type: `git --version`

**macOS:**
```bash
# Using Homebrew
brew install git

# Or download from: https://git-scm.com/download/mac
```

**Linux:**
```bash
sudo apt update
sudo apt install git
```

### 2. Create GitHub Account

1. Go to: https://github.com
2. Click "Sign up"
3. Create account (it's free!)
4. Verify your email

---

## 🚀 Quick Start - Upload Your Project (5 Steps)

### Step 1: Configure Git (One-Time Setup)

Open terminal/command prompt:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the **same email** as your GitHub account!

Verify:
```bash
git config --global --list
```

### Step 2: Initialize Git in Your Project

```bash
cd sentiment-dashboard
git init
```

You should see: "Initialized empty Git repository"

### Step 3: Add All Files

```bash
git add .
```

The `.` means "add everything in this folder"

### Step 4: Make Your First Commit

```bash
git commit -m "Initial commit - Sentiment Dashboard project"
```

A commit is like a "save point" in your project.

### Step 5: Create GitHub Repository & Upload

**On GitHub:**
1. Go to: https://github.com
2. Click the **"+"** icon (top-right) → **"New repository"**
3. Repository name: `sentiment-dashboard`
4. Description: "Real-time sentiment analysis dashboard for stocks"
5. Keep it **Public** (so recruiters can see it!)
6. **DO NOT** check "Add a README" (we already have one)
7. Click **"Create repository"**

**In Your Terminal:**

GitHub will show you commands. Copy and paste them, or use these:

```bash
# Add the GitHub repository as "remote"
git remote add origin https://github.com/YOUR_USERNAME/sentiment-dashboard.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username!

**Enter your GitHub credentials when prompted.**

---

## 🎉 Success!

Go to: `https://github.com/YOUR_USERNAME/sentiment-dashboard`

You should see your project online! 🚀

---

## 📚 Git Basics - Essential Commands

### Check Status (Use This Often!)

```bash
git status
```

Shows:
- Which files changed
- Which files are staged (ready to commit)
- Current branch

### View Your Changes

```bash
git diff
```

Shows exactly what you changed in files.

### Add Files

```bash
# Add specific file
git add backend/app/main.py

# Add all files in a folder
git add backend/

# Add everything
git add .
```

### Commit Changes

```bash
git commit -m "Your descriptive message here"
```

**Good commit messages:**
- ✅ "Add sentiment analysis feature"
- ✅ "Fix MongoDB connection bug"
- ✅ "Update README with setup instructions"

**Bad commit messages:**
- ❌ "Update"
- ❌ "Fix stuff"
- ❌ "asdfasdf"

### Push to GitHub

```bash
git push
```

Uploads your commits to GitHub.

### Pull from GitHub

```bash
git pull
```

Downloads latest changes from GitHub.

### View Commit History

```bash
git log
```

Press `q` to exit.

Short version:
```bash
git log --oneline
```

---

## 🔄 Daily Workflow

### Making Changes:

```bash
# 1. Make changes to your code in VS Code
# ...edit files...

# 2. Check what changed
git status

# 3. Add the changes
git add .

# 4. Commit with message
git commit -m "Add synthetic data generator"

# 5. Push to GitHub
git push
```

### Complete Example:

```bash
# You just finished adding a new feature
cd sentiment-dashboard

# See what changed
git status
# Shows: modified: backend/app/api/collection.py

# Add the changes
git add .

# Commit
git commit -m "Add fallback data collection system"

# Push to GitHub
git push

# Done! Changes are now on GitHub
```

---

## 🌿 Branching (Intermediate)

Branches let you work on features without affecting main code.

### Create a Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-ui

# Now you're on "feature/new-ui" branch
```

### Work on Branch

```bash
# Make changes...
git add .
git commit -m "Redesign dashboard UI"

# Push branch to GitHub
git push -u origin feature/new-ui
```

### Merge Branch (After Feature is Done)

```bash
# Switch back to main
git checkout main

# Merge your feature branch
git merge feature/new-ui

# Push to GitHub
git push

# Delete branch (optional)
git branch -d feature/new-ui
```

---

## 🔧 Common Scenarios

### Scenario 1: Made Mistake, Want to Undo

**Undo changes to a file (before commit):**
```bash
git checkout -- filename.py
```

**Undo last commit (keep changes):**
```bash
git reset --soft HEAD~1
```

**Undo last commit (delete changes - CAREFUL!):**
```bash
git reset --hard HEAD~1
```

### Scenario 2: Accidentally Committed Sensitive Data

**Remove file from Git (but keep on your computer):**
```bash
git rm --cached backend/.env
git commit -m "Remove .env from Git"
git push
```

### Scenario 3: Want to See Old Version

```bash
# List all commits
git log --oneline

# Go back to specific commit (read-only)
git checkout COMMIT_HASH

# Return to latest
git checkout main
```

### Scenario 4: Clone Your Project on Another Computer

```bash
git clone https://github.com/YOUR_USERNAME/sentiment-dashboard.git
cd sentiment-dashboard
```

---

## 🎨 GitHub Features

### README.md

Your README is the first thing people see! Make it great:

- ✅ Project title and description
- ✅ Screenshots/GIFs
- ✅ Installation instructions
- ✅ Usage examples
- ✅ Technologies used
- ✅ Your contact info

We already created a great README for you!

### GitHub Profile

Make your profile stand out:

1. Go to: https://github.com/YOUR_USERNAME
2. Click "Edit profile"
3. Add:
   - Profile picture
   - Bio: "CS Student at Rutgers | Seeking AI/ML roles"
   - Location: "New Jersey"
   - Website: Your portfolio/LinkedIn

### Pin Repositories

1. Go to your profile
2. Click "Customize your pins"
3. Select your best projects (including sentiment-dashboard!)
4. These show first on your profile

---

## 📊 Project Organization

### Good File Structure:

```
sentiment-dashboard/
├── .git/                  (Git folder - don't touch!)
├── .gitignore             (Files to ignore)
├── README.md              (Project description)
├── LICENSE                (Optional: MIT license)
├── backend/
├── frontend/
└── docker-compose.yml
```

### .gitignore (Already Created!)

This file tells Git what NOT to upload:

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# Node
node_modules/
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

Never commit:
- ❌ API keys (.env files)
- ❌ Passwords
- ❌ node_modules/ (too large)
- ❌ Virtual environments
- ❌ Database files

---

## 🎓 Git Commands Cheat Sheet

### Setup & Config
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git init
git clone <url>
```

### Basic Commands
```bash
git status          # Check status
git add .           # Stage all changes
git add <file>      # Stage specific file
git commit -m "msg" # Commit changes
git push            # Upload to GitHub
git pull            # Download from GitHub
```

### Branching
```bash
git branch                    # List branches
git branch <name>             # Create branch
git checkout <name>           # Switch branch
git checkout -b <name>        # Create & switch
git merge <branch>            # Merge branch
git branch -d <branch>        # Delete branch
```

### History
```bash
git log                # Show commits
git log --oneline      # Compact view
git diff               # Show changes
git show <commit>      # Show commit details
```

### Undo
```bash
git checkout -- <file>        # Discard changes
git reset HEAD <file>         # Unstage file
git reset --soft HEAD~1       # Undo last commit (keep changes)
git reset --hard HEAD~1       # Undo last commit (delete changes)
```

---

## 🌟 Best Practices

### 1. Commit Often
- Small, focused commits
- Easier to track changes
- Easier to undo if needed

### 2. Write Good Commit Messages
```bash
# Good
git commit -m "Add user authentication feature"
git commit -m "Fix memory leak in data collection"
git commit -m "Update README with deployment instructions"

# Bad
git commit -m "update"
git commit -m "fix"
git commit -m "changes"
```

### 3. Use Branches for Features
```bash
# Don't work directly on main
git checkout -b feature/sentiment-chart
# ...work...
git checkout main
git merge feature/sentiment-chart
```

### 4. Pull Before Push
```bash
git pull    # Get latest changes
git push    # Upload your changes
```

### 5. Never Commit Secrets
- Always use .gitignore
- Keep .env files local
- Use environment variables

---

## 🚀 Making Your Repository Stand Out

### 1. Add a Great README

We already created one! But customize it:
- Add screenshots of your dashboard
- Add a demo GIF (use LICEcap or Gyazo)
- Link to live demo if deployed

### 2. Add Topics/Tags

On GitHub:
1. Go to your repository
2. Click "⚙️" next to "About"
3. Add topics: `python`, `react`, `sentiment-analysis`, `machine-learning`, `fastapi`

### 3. Add a License

```bash
# Create LICENSE file
# Choose MIT License (most common for portfolio projects)
```

On GitHub:
1. Click "Add file" → "Create new file"
2. Name it: `LICENSE`
3. GitHub will suggest license templates
4. Choose "MIT License"

### 4. Create a Nice GitHub Profile README

1. Create repository: `YOUR_USERNAME/YOUR_USERNAME` (special repo!)
2. Add README.md with:
   - Introduction
   - Skills (Python, React, ML, etc.)
   - Projects (link to sentiment-dashboard!)
   - Contact info

Example:
```markdown
# Hi, I'm Vinh! 👋

🎓 CS Student at Rutgers University
🔍 Seeking AI/ML & Software Engineering roles
💻 Passionate about Data Science and Full-Stack Development

## 🛠️ Tech Stack
- **Languages**: Python, Java, JavaScript, SQL
- **ML/Data**: pandas, scikit-learn, VADER
- **Web**: React, FastAPI, Node.js
- **Tools**: Docker, Git, MongoDB

## 🚀 Featured Projects
- [Sentiment Dashboard](https://github.com/YOUR_USERNAME/sentiment-dashboard) - Real-time stock sentiment analysis

📫 Reach me: vietvinh2432001@gmail.com | [LinkedIn](linkedin.com/in/vinhpham243)
```

---

## 🎬 Complete Workflow Example

Let's say you just finished adding the backup system:

```bash
# 1. Check what changed
git status

# 2. Add all changes
git add .

# 3. Commit with descriptive message
git commit -m "Add intelligent fallback system with synthetic data generation

- Implement synthetic data generator for demo purposes
- Add automatic fallback: Reddit -> Twitter -> Synthetic
- Create comprehensive backup plan documentation
- Add test scripts for fallback system"

# 4. Push to GitHub
git push

# Done! Check GitHub to see your changes
```

**Multi-line commit messages** (optional but professional):
```bash
git commit -m "Add intelligent fallback system" -m "This ensures the app always works even when APIs fail. Includes synthetic data generator with realistic templates."
```

---

## 📱 Using Git in VS Code

VS Code has built-in Git support!

### Visual Interface:

1. **Source Control Panel**: Click icon on left (or `Ctrl+Shift+G`)
2. **See Changes**: Modified files show in list
3. **Stage Changes**: Click `+` next to file
4. **Commit**: Type message in box, click ✓
5. **Push**: Click "..." → "Push"

### VS Code Git Features:

- **File colors**:
  - Green = New file
  - Yellow = Modified file
  - Red = Deleted file
- **Inline changes**: See exact lines changed
- **Compare**: Right-click file → "Compare with..."

---

## 🏆 After You Upload

### Share Your Project:

**On Resume:**
```
Sentiment Analysis Dashboard
https://github.com/YOUR_USERNAME/sentiment-dashboard
- Real-time sentiment analysis using VADER and Reddit API
- Built with FastAPI, React, MongoDB, and Docker
```

**On LinkedIn:**
```
Just completed my Sentiment Dashboard project! 🚀

Built a full-stack application that analyzes social media sentiment for stocks:
- FastAPI backend with RESTful API
- React dashboard with real-time charts
- Intelligent fallback system for reliability
- Docker containerization

Check it out: github.com/YOUR_USERNAME/sentiment-dashboard

#Python #React #MachineLearning #FullStack #OpenToWork
```

---

## ✅ Final Checklist

Before sharing your repository:

- [ ] Good README with project description
- [ ] .gitignore excludes sensitive files
- [ ] No .env file committed
- [ ] Code is well-commented
- [ ] Requirements.txt is up to date
- [ ] Project runs on fresh clone
- [ ] Add LICENSE file
- [ ] Add topics/tags on GitHub
- [ ] Pin repository on your profile

---

## 🆘 Common Issues & Solutions

### "Permission denied (publickey)"

**Solution 1: Use HTTPS instead of SSH**
```bash
# Check current remote
git remote -v

# If it shows git@github.com, change to https
git remote set-url origin https://github.com/YOUR_USERNAME/sentiment-dashboard.git
```

**Solution 2: Set up SSH key** (for advanced users)
Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "Failed to push some refs"

Someone else made changes on GitHub. Pull first:
```bash
git pull --rebase
git push
```

### "Git is not recognized"

Restart your terminal/VS Code after installing Git.

### "Everything up-to-date" but changes not on GitHub

You forgot to commit:
```bash
git add .
git commit -m "Your message"
git push
```

---

## 🎯 Next Steps

1. ✅ Initialize Git in your project
2. ✅ Make first commit
3. ✅ Create GitHub repository
4. ✅ Push to GitHub
5. ✅ Add topics and description
6. ✅ Share on LinkedIn
7. ✅ Add to resume

---

## 📚 Learning Resources

- **GitHub Docs**: https://docs.github.com
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Interactive Tutorial**: https://learngitbranching.js.org/
- **Practice**: https://github.com/skills

---

**You're ready to use Git like a pro!** 🎉

Start with the Quick Start section, then explore more features as you need them.
