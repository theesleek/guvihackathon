import numpy as np
import librosa


def extract_features(y: np.ndarray, sr: int = 16000) -> np.ndarray:
    """
    Extract a simple set of handcrafted audio features:
    - MFCCs (mean & std)
    - Spectral centroid (mean & std)
    - Zero crossing rate (mean)
    This is a lightweight baseline; you can replace or extend this later.
    """
    if y is None or len(y) == 0:
        raise ValueError("Empty audio signal received for feature extraction")

    # MFCCs
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)

    # Spectral centroid
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_centroid_mean = spec_centroid.mean()
    spec_centroid_std = spec_centroid.std()

    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = zcr.mean()

    features = np.concatenate(
        [
            mfcc_mean,
            mfcc_std,
            np.array([spec_centroid_mean, spec_centroid_std, zcr_mean]),
        ]
    )
    return features


