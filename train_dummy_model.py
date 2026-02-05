import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from features import extract_features


def generate_synthetic_waveform(duration_sec: float, sr: int = 16000, ai_like: bool = False) -> np.ndarray:
    """
    Generate a synthetic waveform for demonstration only.
    - "AI-like" signals: smoother, more periodic.
    - "Human-like" signals: more noisy and irregular.
    """
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)

    if ai_like:
        # Smoother, more periodic sinusoidal pattern
        freq = np.random.uniform(150, 300)
        waveform = 0.8 * np.sin(2 * np.pi * freq * t)
    else:
        # Noisy, irregular signal (approximate "human-like" variability)
        freqs = np.random.uniform(80, 500, size=3)
        waveform = sum(
            (0.3 + 0.2 * np.random.rand()) * np.sin(2 * np.pi * f * t)
            for f in freqs
        )
        waveform += 0.3 * np.random.randn(len(t))

    # Normalize
    waveform = waveform / (np.max(np.abs(waveform)) + 1e-6)
    return waveform.astype(np.float32)


def main() -> None:
    sr = 16000
    n_samples_per_class = 100

    X = []
    y = []

    # Generate synthetic "AI_GENERATED" examples
    for _ in range(n_samples_per_class):
        wav = generate_synthetic_waveform(duration_sec=3.0, sr=sr, ai_like=True)
        feats = extract_features(wav, sr=sr)
        X.append(feats)
        y.append("AI_GENERATED")

    # Generate synthetic "HUMAN" examples
    for _ in range(n_samples_per_class):
        wav = generate_synthetic_waveform(duration_sec=3.0, sr=sr, ai_like=False)
        feats = extract_features(wav, sr=sr)
        X.append(feats)
        y.append("HUMAN")

    X = np.stack(X, axis=0)
    y = np.array(y)

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        random_state=42,
    )
    clf.fit(X, y)

    # Save model
    model_path = "baseline_model.joblib"
    joblib.dump(clf, model_path)

    print(f"Saved dummy baseline model to: {model_path}")


if __name__ == "__main__":
    main()


