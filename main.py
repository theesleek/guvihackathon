import base64
import io
import os
from typing import Literal

import librosa
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from features import extract_features
from model import get_model


load_dotenv()

# Load API_KEY from environment variable, fallback to hardcoded for local dev
API_KEY = os.getenv("API_KEY", "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4")

if not API_KEY:
    # For safety in production on Render, API_KEY should be set in env vars.
    # Locally, you must set it in a .env file or environment.
    raise RuntimeError("API_KEY not set. Please define it in environment variables or .env file.")



app = FastAPI(
    title="AI-Generated Voice Detection API",
    version="1.0.0",
    description=(
        "Detect whether a Base64-encoded MP3 voice sample is AI_GENERATED or HUMAN.\n"
        "Supported languages: Tamil (ta), English (en), Hindi (hi), Malayalam (ml), Telugu (te)."
    ),
)


class DetectionRequest(BaseModel):
    audio_base64: str
    language: Literal["ta", "en", "hi", "ml", "te"]


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float
    details: dict


def verify_api_key(x_api_key: str | None) -> None:
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def decode_audio_from_base64(audio_b64: str, target_sr: int = 16000) -> np.ndarray:
    """
    Decode Base64-encoded MP3 bytes into a mono waveform at target_sr.
    """
    try:
        audio_bytes = base64.b64decode(audio_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio data.")

    audio_buffer = io.BytesIO(audio_bytes)

    try:
        y, sr = librosa.load(audio_buffer, sr=None, mono=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load audio: {e}")

    if y is None or len(y) == 0:
        raise HTTPException(status_code=400, detail="Decoded audio is empty.")

    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

    return y


@app.get("/")
async def root():
    return {"message": "AI-Generated Voice Detection API is running."}


@app.post("/detect", response_model=DetectionResponse)
async def detect(
    payload: DetectionRequest,
    x_api_key: str | None = Header(default=None),
):
    # 1. Auth
    verify_api_key(x_api_key)

    # 2. Decode audio
    waveform = decode_audio_from_base64(payload.audio_base64, target_sr=16000)

    # 3. Extract features
    features = extract_features(waveform, sr=16000)

    # 4. Predict using model
    model = get_model()
    label, confidence, model_version = model.predict(features, payload.language)

    # Ensure confidence is float and within [0, 1]
    confidence = float(max(0.0, min(1.0, confidence)))

    return DetectionResponse(
        result=label,
        confidence=confidence,
        details={
            "language": payload.language,
            "model_version": model_version,
        },
    )



