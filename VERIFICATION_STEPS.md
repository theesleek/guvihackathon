# Complete Verification Steps

Follow these exact steps to verify your AI Voice Detection API is working correctly.

---

## Step 1: Verify Project Structure

Ensure you have these files in your project directory:

```
guvi/
├── main.py                 ✓ FastAPI application
├── model.py                ✓ Model wrapper
├── features.py             ✓ Feature extraction
├── train_dummy_model.py    ✓ Training script
├── requirements.txt        ✓ Dependencies
├── render.yaml             ✓ Render deployment config
├── models/
│   └── baseline_model.joblib  ✓ Trained model (created after training)
├── test_api.py             ✓ Test script
├── API_EXAMPLES.md         ✓ API examples
└── VERIFICATION_STEPS.md   ✓ This file
```

---

## Step 2: Install Dependencies

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Expected Output**: All packages install successfully without errors.

---

## Step 3: Train the Model

```powershell
python train_dummy_model.py
```

**Expected Output**:
```
Saved dummy baseline model to: models\baseline_model.joblib
```

**Verify**: Check that `models/baseline_model.joblib` file exists.

---

## Step 4: Start the API Server

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Expected Output**:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Keep this terminal window open** - the server must stay running.

---

## Step 5: Test Root Endpoint

Open a **NEW** PowerShell window and run:

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
```

**Expected Response**:
```json
{
  "message": "AI-Generated Voice Detection API is running."
}
```

**Status Code**: `200 OK`

---

## Step 6: Test Interactive API Docs

Open your browser and go to:
```
http://localhost:8000/docs
```

**Expected**: You should see the Swagger UI with:
- `GET /` endpoint
- `POST /detect` endpoint

---

## Step 7: Test /detect Endpoint (Without Real Audio)

This test will fail with "Invalid base64 audio data" but shows the API structure works:

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"
}

$body = @{
    audio_base64 = "dGVzdA=="
    language = "en"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
```

**Expected Response** (400 Bad Request):
```json
{
  "detail": "Invalid base64 audio data."
}
```

This confirms:
- ✅ API endpoint is accessible
- ✅ Authentication works
- ✅ Request validation works
- ✅ Error handling works

---

## Step 8: Test with Real MP3 File

### 8a. Prepare an MP3 File

Place a sample MP3 file in your project directory (e.g., `sample.mp3`).

### 8b. Convert MP3 to Base64

```powershell
$base64Audio = [Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3"))
$base64Audio | Out-File -Encoding utf8 audio_base64.txt
```

### 8c. Make API Request

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"
}

$base64Audio = Get-Content audio_base64.txt -Raw

$body = @{
    audio_base64 = $base64Audio.Trim()
    language = "en"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 10
```

**Expected Response** (200 OK):
```json
{
  "result": "HUMAN",
  "confidence": 0.7234,
  "details": {
    "language": "en",
    "model_version": "baseline-v1"
  }
}
```

**OR**

```json
{
  "result": "AI_GENERATED",
  "confidence": 0.6543,
  "details": {
    "language": "en",
    "model_version": "baseline-v1"
  }
}
```

---

## Step 9: Test Invalid API Key

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "wrong_key_12345"
}

$body = @{
    audio_base64 = "dGVzdA=="
    language = "en"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
} catch {
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
    Write-Host "Error: $($_.ErrorDetails.Message)"
}
```

**Expected**: `401 Unauthorized` with message "Invalid or missing API key."

---

## Step 10: Test Different Languages

Test with different language codes:

```powershell
$languages = @("ta", "en", "hi", "ml", "te")

foreach ($lang in $languages) {
    Write-Host "Testing language: $lang"
    
    $body = @{
        audio_base64 = $base64Audio.Trim()
        language = $lang
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
    Write-Host "Result: $($response.result), Confidence: $($response.confidence)"
    Write-Host "---"
}
```

---

## Step 11: Run Automated Test Script

```powershell
pip install requests
python test_api.py
```

This will run multiple tests automatically.

---

## Verification Checklist

- [ ] All dependencies installed successfully
- [ ] Model trained (`models/baseline_model.joblib` exists)
- [ ] Server starts without errors
- [ ] Root endpoint (`GET /`) returns 200 OK
- [ ] Interactive docs (`/docs`) accessible in browser
- [ ] `/detect` endpoint accepts requests
- [ ] Authentication works (valid API key)
- [ ] Authentication rejects invalid API key (401)
- [ ] Request validation works (invalid audio returns 400)
- [ ] Real MP3 file processes successfully (200 OK)
- [ ] Response contains `result`, `confidence`, and `details`
- [ ] All 5 languages work (`ta`, `en`, `hi`, `ml`, `te`)

---

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Try a different port: `--port 8001`
- Check for Python syntax errors: `python -m py_compile main.py`

### "Module not found" errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Model file not found" warnings
- Run: `python train_dummy_model.py`
- Verify `models/baseline_model.joblib` exists

### API returns 401 Unauthorized
- Check API key matches: `f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4`
- Verify header name is exactly: `x-api-key`

### API returns 400 Bad Request
- Verify base64 string is valid
- Ensure MP3 file is not corrupted
- Check audio file is actually an MP3 format

---

## Next Steps

Once verified locally:
1. Push to GitHub
2. Deploy on Render
3. Test production endpoint
4. Improve model with real training data

See `README.md` for deployment instructions.

