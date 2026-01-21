#!/bin/bash

# Git Setup Helper Script
# This script helps you initialize Git and push to GitHub

echo "======================================"
echo "   Git Setup Helper for Sentiment    "
echo "        Dashboard Project             "
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed!${NC}"
    echo ""
    echo "Please install Git first:"
    echo "  Windows: https://git-scm.com/download/win"
    echo "  macOS:   brew install git"
    echo "  Linux:   sudo apt install git"
    exit 1
fi

echo -e "${GREEN}✅ Git is installed!${NC}"
echo ""

# Check if already a git repository
if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  Git repository already initialized${NC}"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    echo -e "${BLUE}Initializing Git repository...${NC}"
    git init
    echo ""
fi

# Get user information
echo -e "${BLUE}Git Configuration${NC}"
echo "=================="
echo ""

read -p "Enter your name (for Git commits): " GIT_NAME
read -p "Enter your email (same as GitHub): " GIT_EMAIL

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo ""
echo -e "${GREEN}✅ Git configured!${NC}"
echo "   Name:  $GIT_NAME"
echo "   Email: $GIT_EMAIL"
echo ""

# Stage and commit
echo -e "${BLUE}Preparing initial commit...${NC}"
git add .

echo ""
echo "Files to commit:"
git status --short
echo ""

read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Initial commit - Sentiment Dashboard project"
fi

git commit -m "$COMMIT_MSG"
echo ""
echo -e "${GREEN}✅ Initial commit created!${NC}"
echo ""

# Get GitHub username
echo -e "${BLUE}GitHub Setup${NC}"
echo "============"
echo ""
echo "Before continuing, make sure you have:"
echo "  1. Created a GitHub account"
echo "  2. Created a new repository called 'sentiment-dashboard'"
echo "  3. Set the repository to PUBLIC (so recruiters can see it)"
echo ""
read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Please create a GitHub repository first:${NC}"
    echo "  1. Go to: https://github.com"
    echo "  2. Click '+' → 'New repository'"
    echo "  3. Name it: sentiment-dashboard"
    echo "  4. Keep it PUBLIC"
    echo "  5. DO NOT check 'Add a README'"
    echo "  6. Click 'Create repository'"
    echo ""
    echo "Then run this script again!"
    exit 0
fi

echo ""
read -p "Enter your GitHub username: " GITHUB_USER

# Add remote
GITHUB_URL="https://github.com/$GITHUB_USER/sentiment-dashboard.git"
echo ""
echo -e "${BLUE}Adding GitHub remote...${NC}"

# Check if remote already exists
if git remote | grep -q "origin"; then
    git remote set-url origin $GITHUB_URL
    echo "Remote URL updated to: $GITHUB_URL"
else
    git remote add origin $GITHUB_URL
    echo "Remote added: $GITHUB_URL"
fi

echo ""
echo -e "${BLUE}Pushing to GitHub...${NC}"
echo ""
echo "You may be asked for your GitHub password."
echo "If using 2FA, you'll need a Personal Access Token instead of password."
echo ""

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo "   🎉 SUCCESS! 🎉"
    echo "======================================${NC}"
    echo ""
    echo "Your project is now on GitHub!"
    echo ""
    echo -e "${GREEN}View it at:${NC}"
    echo "  https://github.com/$GITHUB_USER/sentiment-dashboard"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Add topics to your repo (python, react, machine-learning)"
    echo "  2. Pin it on your GitHub profile"
    echo "  3. Add the link to your resume"
    echo "  4. Share on LinkedIn!"
    echo ""
    echo -e "${BLUE}Daily workflow:${NC}"
    echo "  git add ."
    echo "  git commit -m 'Your message'"
    echo "  git push"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Push failed!${NC}"
    echo ""
    echo -e "${YELLOW}Common issues:${NC}"
    echo "  1. Wrong username/password"
    echo "  2. Repository doesn't exist on GitHub"
    echo "  3. Need Personal Access Token (if using 2FA)"
    echo ""
    echo "To create a Personal Access Token:"
    echo "  1. GitHub → Settings → Developer settings"
    echo "  2. Personal access tokens → Generate new token"
    echo "  3. Select 'repo' scope"
    echo "  4. Use token as password"
    echo ""
fi
