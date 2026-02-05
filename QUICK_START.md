# Quick Start Guide - Exact Commands

Copy and paste these commands exactly as shown.

---

## 1. Setup (One-time)

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train_dummy_model.py
```

---

## 2. Start Server

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Keep this window open!**

---

## 3. Test in Browser

Open: `http://localhost:8000/docs`

---

## 4. Test with PowerShell (New Window)

### Test Root Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
```

### Test /detect Endpoint (Replace with your MP3 file path)

```powershell
# Step 1: Convert MP3 to Base64
$base64Audio = [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\path\to\your\sample.mp3"))

# Step 2: Make API Request
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"
}

$body = @{
    audio_base64 = $base64Audio
    language = "en"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 10
```

---

## 5. Complete Example (All-in-One)

```powershell
# Set your MP3 file path here
$mp3Path = "sample.mp3"

# Convert to base64
$base64Audio = [Convert]::ToBase64String([IO.File]::ReadAllBytes($mp3Path))

# API Configuration
$apiUrl = "http://localhost:8000/detect"
$apiKey = "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"

# Headers
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = $apiKey
}

# Request Body
$body = @{
    audio_base64 = $base64Audio
    language = "en"  # Change to: "ta", "hi", "ml", or "te" for other languages
} | ConvertTo-Json

# Make Request
try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Headers $headers -Body $body
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Result: $($response.result)" -ForegroundColor Cyan
    Write-Host "Confidence: $($response.confidence)" -ForegroundColor Cyan
    Write-Host "Language: $($response.details.language)" -ForegroundColor Cyan
    Write-Host "Model Version: $($response.details.model_version)" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    }
}
```

---

## API Key

**Current API Key**: `f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4`

**To generate a new one**:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then update `main.py` line 19 or set environment variable `API_KEY`.

---

## Supported Languages

- `"ta"` - Tamil
- `"en"` - English  
- `"hi"` - Hindi
- `"ml"` - Malayalam
- `"te"` - Telugu

---

## Expected Response Format

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

**Possible `result` values**:
- `"AI_GENERATED"`
- `"HUMAN"`

**`confidence`**: Float between 0.0 and 1.0

---

## Common Errors

### 401 Unauthorized
- Check API key is correct
- Check header name is exactly `x-api-key`

### 400 Bad Request
- Verify MP3 file is valid
- Check base64 encoding is correct
- Ensure language code is one of: `ta`, `en`, `hi`, `ml`, `te`

### Connection Refused
- Make sure server is running
- Check port 8000 is not blocked
- Try `http://127.0.0.1:8000` instead of `localhost`

