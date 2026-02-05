# API Testing Examples

Complete examples for testing the AI Voice Detection API.

## API Configuration

- **Base URL (Local)**: `http://localhost:8000`
- **Base URL (Render)**: `https://your-service-name.onrender.com`
- **API Key**: `f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4`

---

## Endpoint: GET /

**Description**: Health check endpoint

### Request (PowerShell)
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET
```

### Request (curl)
```bash
curl http://localhost:8000/
```

### Response
```json
{
  "message": "AI-Generated Voice Detection API is running."
}
```

---

## Endpoint: POST /detect

**Description**: Detect if audio is AI_GENERATED or HUMAN

### Request Headers
```
Content-Type: application/json
x-api-key: f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4
```

### Request Body
```json
{
  "audio_base64": "<BASE64_ENCODED_MP3_STRING>",
  "language": "en"
}
```

**Supported Languages**:
- `"ta"` - Tamil
- `"en"` - English
- `"hi"` - Hindi
- `"ml"` - Malayalam
- `"te"` - Telugu

---

## Example 1: PowerShell - Convert MP3 to Base64 and Test

### Step 1: Convert MP3 to Base64
```powershell
# Save base64 to file
[Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3")) | Out-File -Encoding utf8 audio_base64.txt

# Or get it directly in a variable
$base64Audio = [Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3"))
```

### Step 2: Make API Request
```powershell
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

### Expected Response
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

---

## Example 2: curl (Windows CMD)

### Step 1: Convert MP3 to Base64
```cmd
certutil -encode sample.mp3 audio_base64.txt
```
Then copy the content (remove header/footer lines if present).

### Step 2: Make API Request
```cmd
curl -X POST "http://localhost:8000/detect" ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4" ^
  -d "{\"audio_base64\": \"<PASTE_BASE64_HERE>\", \"language\": \"en\"}"
```

---

## Example 3: Python Script

```python
import base64
import requests

# Read MP3 file
with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

# API request
url = "http://localhost:8000/detect"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"
}
payload = {
    "audio_base64": audio_base64,
    "language": "en"  # or "ta", "hi", "ml", "te"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

---

## Example 4: JavaScript/Node.js

```javascript
const fs = require('fs');
const axios = require('axios');

// Read and encode MP3
const audioBuffer = fs.readFileSync('sample.mp3');
const audioBase64 = audioBuffer.toString('base64');

// Make request
axios.post('http://localhost:8000/detect', {
    audio_base64: audioBase64,
    language: 'en'
}, {
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4'
    }
})
.then(response => {
    console.log(response.data);
})
.catch(error => {
    console.error(error.response.data);
});
```

---

## Example 5: Using FastAPI Interactive Docs

1. Start the server: `uvicorn main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click on `POST /detect`
4. Click "Try it out"
5. Enter:
   - **x-api-key**: `f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4`
   - **Request body**:
     ```json
     {
       "audio_base64": "<your_base64_string>",
       "language": "en"
     }
     ```
6. Click "Execute"

---

## Error Responses

### 401 Unauthorized (Invalid API Key)
```json
{
  "detail": "Invalid or missing API key."
}
```

### 400 Bad Request (Invalid Audio)
```json
{
  "detail": "Invalid base64 audio data."
}
```

or

```json
{
  "detail": "Failed to load audio: <error_message>"
}
```

---

## Testing Different Languages

Replace `"language"` in the request body:

- **Tamil**: `"language": "ta"`
- **English**: `"language": "en"`
- **Hindi**: `"language": "hi"`
- **Malayalam**: `"language": "ml"`
- **Telugu**: `"language": "te"`

---

## Quick Test Commands

### Test Root Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
```

### Test with Invalid API Key
```powershell
$headers = @{"x-api-key" = "wrong_key"}
$body = @{audio_base64 = "test"; language = "en"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/detect" -Method POST -Headers $headers -Body $body
```

Expected: `401 Unauthorized`

