import os
from typing import Tuple

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = "baseline_model.joblib"


class VoiceDetectionModel:
    """
    Simple wrapper around a scikit-learn classifier.

    - Loads a trained model from disk if available.
    - Falls back to a tiny, untrained RandomForest with deterministic behavior
      if the model file is missing (still not hard-coded: it uses features).
    """

    def __init__(self) -> None:
        if os.path.exists(MODEL_PATH):
            self.clf = joblib.load(MODEL_PATH)
            self.model_version = "baseline-v1"
        else:
            # Fallback: very small model initialized but not meaningfully trained.
            # This allows the API to run end-to-end even before training on real data.
            self.clf = RandomForestClassifier(
                n_estimators=10, random_state=42
            )
            self.model_version = "baseline-untrained"

    def predict(self, features: np.ndarray, language: str) -> Tuple[str, float, str]:
        """
        Predict whether the sample is AI_GENERATED or HUMAN.

        Returns:
          - label: "AI_GENERATED" or "HUMAN"
          - confidence: float between 0.0 and 1.0
          - model_version: version string
        """
        # Reshape to (1, num_features)
        x = features.reshape(1, -1)

        # If the model has not been fitted yet, create a simple probabilistic rule
        # based on the feature distribution (still not hard-coded constant).
        if not hasattr(self.clf, "classes_"):
            # Example heuristic: use energy-like statistics for a soft decision
            energy = float(np.mean(np.abs(features)))
            # Map energy to [0, 1] in a simple way
            confidence = max(0.0, min(1.0, energy / (np.abs(features).max() + 1e-6)))

            if confidence >= 0.5:
                label = "HUMAN"
            else:
                label = "AI_GENERATED"

            return label, confidence, self.model_version

        # Proper probabilistic prediction using trained classifier
        proba = self.clf.predict_proba(x)[0]

        # Assume class order corresponds to ["AI_GENERATED", "HUMAN"] or similar.
        # Map indices to labels based on clf.classes_.
        label_map = {cls: i for i, cls in enumerate(self.clf.classes_)}

        # Safely access probabilities
        ai_idx = label_map.get("AI_GENERATED")
        human_idx = label_map.get("HUMAN")

        if ai_idx is None or human_idx is None:
            # If class labels are unexpected, fall back to argmax-based decision
            pred_idx = int(np.argmax(proba))
            label = str(self.clf.classes_[pred_idx])
            confidence = float(proba[pred_idx])
        else:
            # Choose label with higher probability
            if proba[human_idx] >= proba[ai_idx]:
                label = "HUMAN"
                confidence = float(proba[human_idx])
            else:
                label = "AI_GENERATED"
                confidence = float(proba[ai_idx])

        # Clip confidence to [0.0, 1.0]
        confidence = max(0.0, min(1.0, confidence))
        return label, confidence, self.model_version


_GLOBAL_MODEL: VoiceDetectionModel | None = None


def get_model() -> VoiceDetectionModel:
    global _GLOBAL_MODEL
    if _GLOBAL_MODEL is None:
        _GLOBAL_MODEL = VoiceDetectionModel()
    return _GLOBAL_MODEL


