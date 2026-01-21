@echo off
REM Git Setup Helper Script for Windows
REM This script helps you initialize Git and push to GitHub

echo ======================================
echo    Git Setup Helper for Sentiment
echo         Dashboard Project
echo ======================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo   Download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed!
echo.

REM Check if already a git repository
if exist .git (
    echo [WARNING] Git repository already initialized
    echo.
    set /p continue="Do you want to continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 0
) else (
    echo Initializing Git repository...
    git init
    echo.
)

REM Get user information
echo Git Configuration
echo ==================
echo.

set /p GIT_NAME="Enter your name (for Git commits): "
set /p GIT_EMAIL="Enter your email (same as GitHub): "

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo.
echo [OK] Git configured!
echo    Name:  %GIT_NAME%
echo    Email: %GIT_EMAIL%
echo.

REM Stage and commit
echo Preparing initial commit...
git add .

echo.
echo Files to commit:
git status --short
echo.

set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit - Sentiment Dashboard project

git commit -m "%COMMIT_MSG%"
echo.
echo [OK] Initial commit created!
echo.

REM Get GitHub username
echo GitHub Setup
echo ============
echo.
echo Before continuing, make sure you have:
echo   1. Created a GitHub account
echo   2. Created a new repository called 'sentiment-dashboard'
echo   3. Set the repository to PUBLIC (so recruiters can see it)
echo.
set /p repo_created="Have you created the GitHub repository? (y/n): "

if /i not "%repo_created%"=="y" (
    echo.
    echo Please create a GitHub repository first:
    echo   1. Go to: https://github.com
    echo   2. Click '+' -^> 'New repository'
    echo   3. Name it: sentiment-dashboard
    echo   4. Keep it PUBLIC
    echo   5. DO NOT check 'Add a README'
    echo   6. Click 'Create repository'
    echo.
    echo Then run this script again!
    pause
    exit /b 0
)

echo.
set /p GITHUB_USER="Enter your GitHub username: "

REM Add remote
set GITHUB_URL=https://github.com/%GITHUB_USER%/sentiment-dashboard.git
echo.
echo Adding GitHub remote...

git remote | findstr "origin" >nul 2>&1
if %errorlevel% equ 0 (
    git remote set-url origin %GITHUB_URL%
    echo Remote URL updated to: %GITHUB_URL%
) else (
    git remote add origin %GITHUB_URL%
    echo Remote added: %GITHUB_URL%
)

echo.
echo Pushing to GitHub...
echo.
echo You may be asked for your GitHub password.
echo If using 2FA, you'll need a Personal Access Token instead.
echo.

git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo    SUCCESS!
    echo ======================================
    echo.
    echo Your project is now on GitHub!
    echo.
    echo View it at:
    echo   https://github.com/%GITHUB_USER%/sentiment-dashboard
    echo.
    echo Next steps:
    echo   1. Add topics to your repo (python, react, machine-learning)
    echo   2. Pin it on your GitHub profile
    echo   3. Add the link to your resume
    echo   4. Share on LinkedIn!
    echo.
    echo Daily workflow:
    echo   git add .
    echo   git commit -m "Your message"
    echo   git push
    echo.
) else (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo   1. Wrong username/password
    echo   2. Repository doesn't exist on GitHub
    echo   3. Need Personal Access Token (if using 2FA)
    echo.
    echo To create a Personal Access Token:
    echo   1. GitHub -^> Settings -^> Developer settings
    echo   2. Personal access tokens -^> Generate new token
    echo   3. Select 'repo' scope
    echo   4. Use token as password
    echo.
)

pause
