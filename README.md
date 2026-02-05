## AI-Generated Voice Detection API

Python FastAPI service that detects whether an input voice sample is **AI_GENERATED** or **HUMAN** from a Base64-encoded MP3.  
Supported languages: **Tamil (ta), English (en), Hindi (hi), Malayalam (ml), Telugu (te)**.

This repo is structured so you can:
- Run locally for development
- Push to GitHub
- Deploy to **Render** as a web service

> Note: The included model is a simple **baseline** using handcrafted audio features and a lightweight classifier trained on synthetic data. It is **not** production-grade but provides a complete, non-hardcoded pipeline you can later retrain with real data.

---

## Project Structure

```text
.
├── main.py              # FastAPI app entrypoint
├── model.py             # Model loading & prediction logic
├── features.py          # Audio feature extraction utilities
├── train_dummy_model.py # Example: trains a tiny baseline model (synthetic data)
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── render.yaml          # Render deployment configuration
└── README.md            # This file
```

---

## API Specification

- **Endpoint**: `POST /detect`
- **Auth**: HTTP header `x-api-key: <YOUR_API_KEY>`
- **Request body (JSON)**:

```json
{
  "audio_base64": "<BASE64_ENCODED_MP3>",
  "language": "en"
}
```

Where `language` is one of:
- `ta` – Tamil
- `en` – English
- `hi` – Hindi
- `ml` – Malayalam
- `te` – Telugu

- **Response body (JSON)**:

```json
{
  "result": "AI_GENERATED",
  "confidence": 0.81,
  "details": {
    "language": "en",
    "model_version": "baseline-v1"
  }
}
```

---

## 1. Local Setup (Step-by-Step)

### 1.1. Clone or create this project

In your machine (Windows PowerShell, from your `guvi` folder):

```powershell
cd "C:\Users\aisek\OneDrive\Desktop\guvi"
```

If you already have these files locally (via Cursor), just ensure you are in the project folder.  
Otherwise, you can create a new folder and place the files there:

```powershell
mkdir ai-voice-detector
cd ai-voice-detector
```

### 1.2. Create & activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 1.3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 1.4. Configure environment variables

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Edit `.env` and set a strong secret value:

```text
API_KEY=CHANGE_THIS_TO_A_STRONG_SECRET
```

### 1.5. (Optional) Re-train the dummy model

The repo includes a script that trains a very simple baseline classifier on synthetic data (for demonstration only):

```powershell
python train_dummy_model.py
```

This will create a file:

- `models/baseline_model.joblib`

The API will automatically load this file if present.

### 1.6. Run the API locally

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open the interactive docs in a browser:

- `http://localhost:8000/docs`

### 1.7. Example request

Encode an MP3 file to Base64 (PowerShell):

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3")) > audio.txt
```

Copy the Base64 string from `audio.txt`, then call the API:

```powershell
curl -X POST "http://localhost:8000/detect" ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: CHANGE_THIS_TO_A_STRONG_SECRET" ^
  -d "{\"audio_base64\": \"<PASTE_BASE64_HERE>\", \"language\": \"en\"}"
```

You should receive a JSON response with `result`, `confidence`, and `details`.

---

## 2. Prepare for GitHub

From the project root:

```powershell
git init
git add .
git commit -m "Initial AI voice detection API"
```

Then create a new repository on GitHub (via the GitHub website), e.g. `ai-voice-detector`.

Follow the instructions GitHub gives you, typically:

```powershell
git remote add origin https://github.com/<your-username>/ai-voice-detector.git
git branch -M main
git push -u origin main
```

Now your project is on GitHub and ready for Render.

---

## 3. Deploying to Render (Step-by-Step)

1. **Push code to GitHub** (as described above).
2. Go to [Render](https://render.com) and sign in.
3. Click **New +** → **Web Service**.
4. Choose **Build and deploy from a Git repository** and connect your GitHub account.
5. Select your `ai-voice-detector` repository.
6. Configure the service:
   - **Name**: `ai-voice-detector` (any name is fine)
   - **Region**: Choose nearest to you
   - **Branch**: `main`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**:  
     `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Under **Environment Variables**, add:
   - `API_KEY` → same value you used locally (a strong secret).
8. Click **Create Web Service**.

Render will build and deploy the app. Once it’s live, you’ll get a public URL like:

- `https://ai-voice-detector.onrender.com`

Your final public endpoint will be:

- `POST https://ai-voice-detector.onrender.com/detect`

Remember to always include the `x-api-key` header in requests.

---

## 4. How to Improve the Model (Later)

This repo is intentionally simple so you can extend it:

- Replace synthetic training in `train_dummy_model.py` with **real human vs AI-generated** speech in Tamil, English, Hindi, Malayalam, and Telugu.
- Keep using `features.py` or switch to a **deep learning audio model** (e.g. Wav2Vec2).
- Update `model.py` to load your improved model and bump `model_version` in responses.

The API contract (request/response format) and deployment flow can stay the same while you iterate on the model.


