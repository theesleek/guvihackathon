# Exact Commands to Upload to GitHub with Correct Folder Structure

Copy and paste these commands **one by one** in PowerShell.

---

## Step 1: Navigate to Project

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"
```

---

## Step 2: Initialize Git (if not done)

```powershell
git init
```

---

## Step 3: Verify Models Folder Exists

```powershell
Test-Path "models\baseline_model.joblib"
```

**Should return**: `True`

If `False`, run:
```powershell
python train_dummy_model.py
```

---

## Step 4: Add ALL Files (Including Models Folder)

```powershell
# Add everything
git add .

# Explicitly ensure models folder is added
git add models/
git add models/baseline_model.joblib
```

---

## Step 5: Verify Models Folder is Tracked

```powershell
git ls-files | Select-String "models"
```

**Should show**:
```
models/baseline_model.joblib
```

If nothing shows, run:
```powershell
git add -f models/baseline_model.joblib
git status
```

---

## Step 6: Check What Will Be Committed

```powershell
git status
```

**You should see**:
- `models/baseline_model.joblib` listed as a new file
- All your `.py` files
- All your `.md` files
- `requirements.txt`
- `render.yaml`
- `.gitignore`

---

## Step 7: Commit

```powershell
git commit -m "Initial commit: AI Voice Detection API"
```

---

## Step 8: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `ai-voice-detector` (or your choice)
3. **DO NOT** check "Initialize with README"
4. Click "Create repository"

---

## Step 9: Connect and Push

**Replace `YOUR_USERNAME` with your GitHub username:**

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detector.git
git branch -M main
git push -u origin main
```

---

## Step 10: Verify on GitHub

After pushing, go to your repository on GitHub. You should see:

```
📁 models/
  └── baseline_model.joblib
📄 main.py
📄 model.py
📄 features.py
📄 train_dummy_model.py
📄 requirements.txt
📄 render.yaml
📄 README.md
📄 .gitignore
... (other files)
```

---

## Troubleshooting: Models Folder Still Missing

If the `models/` folder doesn't appear on GitHub:

### Solution 1: Force Add

```powershell
git rm -r --cached models/ 2>$null
git add -f models/baseline_model.joblib
git commit -m "Add models folder"
git push
```

### Solution 2: Check .gitignore

```powershell
Get-Content .gitignore | Select-String "models"
```

If it shows `models/` or `*.joblib`, remove those lines from `.gitignore`.

### Solution 3: Create .gitkeep

```powershell
# If model file is missing, create a placeholder
New-Item -Path "models\.gitkeep" -ItemType File -Force
git add models/.gitkeep
git commit -m "Add models folder structure"
git push
```

---

## Complete One-Liner (After Git Init)

If you've already initialized git, run this:

```powershell
git add . ; git add models/ ; git add models/* ; git status
```

This ensures everything including the models folder is added.

---

## Verify Before Pushing

Before pushing, always check:

```powershell
git ls-files
```

This shows ALL files that will be uploaded. Make sure you see:
- `models/baseline_model.joblib` ✅

If you don't see it, the folder won't appear on GitHub!

