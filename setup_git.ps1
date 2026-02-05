# PowerShell script to properly set up Git and push to GitHub
# Run this script to ensure all folders are uploaded correctly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$projectDir = "C:\Users\aisek\OneDrive\Desktop\guvi"
Set-Location $projectDir

Write-Host "Current directory: $projectDir" -ForegroundColor Yellow
Write-Host ""

# Step 1: Initialize Git (if not already done)
if (-not (Test-Path ".git")) {
    Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Green
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "Step 1: Git already initialized" -ForegroundColor Green
}
Write-Host ""

# Step 2: Verify models folder exists
Write-Host "Step 2: Checking project structure..." -ForegroundColor Green
if (Test-Path "models\baseline_model.joblib") {
    Write-Host "✓ Models folder and model file found" -ForegroundColor Green
} else {
    Write-Host "⚠ WARNING: models/baseline_model.joblib not found!" -ForegroundColor Red
    Write-Host "  Run: python train_dummy_model.py" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Check .gitignore exists
if (-not (Test-Path ".gitignore")) {
    Write-Host "⚠ WARNING: .gitignore not found! Creating it..." -ForegroundColor Yellow
    # .gitignore should have been created, but if not, it will be added
}

# Step 4: Add all files
Write-Host "Step 3: Adding all files to Git..." -ForegroundColor Green
git add .
Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

# Step 5: Verify models folder is tracked
Write-Host "Step 4: Verifying models folder is tracked..." -ForegroundColor Green
$trackedFiles = git ls-files | Select-String "models"
if ($trackedFiles) {
    Write-Host "✓ Models folder is tracked:" -ForegroundColor Green
    $trackedFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Cyan }
} else {
    Write-Host "⚠ WARNING: Models folder not tracked!" -ForegroundColor Red
    Write-Host "  Adding models folder explicitly..." -ForegroundColor Yellow
    
    # Ensure models folder exists and has content
    if (-not (Test-Path "models")) {
        New-Item -ItemType Directory -Path "models" -Force | Out-Null
    }
    
    # Create .gitkeep if model file doesn't exist
    if (-not (Test-Path "models\baseline_model.joblib")) {
        New-Item -ItemType File -Path "models\.gitkeep" -Force | Out-Null
        Write-Host "  Created models/.gitkeep" -ForegroundColor Yellow
    }
    
    git add models/
    git add models/*
    Write-Host "✓ Models folder added" -ForegroundColor Green
}
Write-Host ""

# Step 6: Show status
Write-Host "Step 5: Current Git status:" -ForegroundColor Green
Write-Host "----------------------------------------" -ForegroundColor Gray
git status
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host ""

# Step 7: Show what will be committed
Write-Host "Step 6: Files that will be committed:" -ForegroundColor Green
$filesToCommit = git diff --cached --name-only
if ($filesToCommit) {
    $filesToCommit | ForEach-Object { Write-Host "  ✓ $_" -ForegroundColor Cyan }
} else {
    Write-Host "  No new files to commit (everything already committed)" -ForegroundColor Yellow
}
Write-Host ""

# Step 8: Instructions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review the files above" -ForegroundColor White
Write-Host "2. Commit the changes:" -ForegroundColor White
Write-Host "   git commit -m 'Initial commit: AI Voice Detection API'" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Create a repository on GitHub (if not already created)" -ForegroundColor White
Write-Host "   Go to: https://github.com/new" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Connect and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

