# GitHub Setup Guide - Preserve Folder Structure

Follow these exact steps to upload your project to GitHub with the correct folder structure.

---

## Step 1: Initialize Git Repository

Open PowerShell in your project directory:

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"

# Initialize git (if not already done)
git init
```

---

## Step 2: Check Current Status

```powershell
git status
```

This shows which files are tracked/untracked.

---

## Step 3: Add All Files (Including Folders)

```powershell
# Add all files including the models folder
git add .

# Verify what will be committed
git status
```

**Expected output should show**:
- ✅ `main.py`
- ✅ `model.py`
- ✅ `features.py`
- ✅ `train_dummy_model.py`
- ✅ `requirements.txt`
- ✅ `render.yaml`
- ✅ `README.md`
- ✅ `models/baseline_model.joblib` ← **Important: This folder should appear**
- ✅ All other `.md` files
- ✅ `.gitignore`

---

## Step 4: Commit Files

```powershell
git commit -m "Initial commit: AI Voice Detection API"
```

---

## Step 5: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-voice-detector` (or your preferred name)
3. **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

---

## Step 6: Connect and Push

```powershell
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detector.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 7: Verify Folder Structure on GitHub

After pushing, check your GitHub repository. You should see:

```
ai-voice-detector/
├── .gitignore
├── main.py
├── model.py
├── features.py
├── train_dummy_model.py
├── requirements.txt
├── render.yaml
├── README.md
├── API_EXAMPLES.md
├── QUICK_START.md
├── VERIFICATION_STEPS.md
├── test_api.py
└── models/
    └── baseline_model.joblib
```

---

## Troubleshooting: Models Folder Not Showing

If the `models/` folder is not appearing on GitHub:

### Option 1: Force Add Empty Folder

```powershell
# Create a .gitkeep file in models folder
New-Item -Path "models\.gitkeep" -ItemType File -Force

# Add it
git add models/.gitkeep
git add models/baseline_model.joblib
git commit -m "Add models folder and trained model"
git push
```

### Option 2: Check .gitignore

Make sure `.gitignore` doesn't have `models/` or `*.joblib` in it. Check:

```powershell
Get-Content .gitignore
```

If `models/` is listed, remove that line.

### Option 3: Explicitly Add Models Folder

```powershell
# Remove from git cache if needed
git rm -r --cached models/

# Re-add explicitly
git add models/
git add models/baseline_model.joblib
git commit -m "Add models folder structure"
git push
```

---

## Complete Command Sequence (Copy-Paste)

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"

# Initialize (if needed)
git init

# Check status
git status

# Add all files
git add .

# Verify models folder is included
git status | Select-String "models"

# Commit
git commit -m "Initial commit: AI Voice Detection API with models"

# Add remote (CHANGE YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detector.git

# Push
git branch -M main
git push -u origin main
```

---

## Verify Files Are Tracked

Before pushing, verify the models folder is included:

```powershell
git ls-files | Select-String "models"
```

Should show:
```
models/baseline_model.joblib
```

---

## Important Notes

1. **`.env` file**: Should NOT be uploaded (it's in `.gitignore`). Only `.env.example` should be committed.

2. **`models/` folder**: MUST be uploaded because it contains the trained model file.

3. **`__pycache__/`**: Should NOT be uploaded (it's in `.gitignore`).

4. **`venv/`**: Should NOT be uploaded (it's in `.gitignore`).

---

## If You Already Pushed Without Models Folder

If you already pushed and the models folder is missing:

```powershell
# Add models folder
git add models/
git add models/baseline_model.joblib

# Commit
git commit -m "Add models folder and trained model"

# Push
git push
```

---

## Check What Will Be Pushed

Before pushing, see exactly what will be committed:

```powershell
git status
```

All files should show as "new file" or "modified". If `models/` is missing, use the troubleshooting steps above.

