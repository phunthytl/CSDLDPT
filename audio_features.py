import math
from pathlib import Path

import librosa
import numpy as np

SAMPLE_RATE = 22050
WINDOW_SECONDS = 5.0
HOP_SECONDS = 2.5
N_MFCC = 13
FEATURE_DIMENSION = 38


def load_audio(path):
    y, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    return y.astype(np.float32), sr


def _safe_mean(values):
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0 or not np.isfinite(arr).any():
        return 0.0
    return float(np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0).mean())


def _safe_vector(values, size):
    arr = np.asarray(values, dtype=np.float64).reshape(-1)
    if arr.size < size:
        arr = np.pad(arr, (0, size - arr.size))
    arr = arr[:size]
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0).astype(float).tolist()


def extract_segment_features(segment, sr):
    if segment.size == 0:
        raise ValueError("Empty audio segment")

    zcr = _safe_mean(librosa.feature.zero_crossing_rate(y=segment))
    rms = _safe_mean(librosa.feature.rms(y=segment))
    onset_env = librosa.onset.onset_strength(y=segment, sr=sr)
    onset_strength = _safe_mean(onset_env)

    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="frames")
    if onset_frames.size > 1:
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        intervals = np.diff(onset_times)
        tempo = float(60.0 / np.median(intervals[intervals > 0])) if np.any(intervals > 0) else 0.0
    else:
        tempo = 0.0

    spectral_centroid = _safe_mean(librosa.feature.spectral_centroid(y=segment, sr=sr))
    spectral_bandwidth = _safe_mean(librosa.feature.spectral_bandwidth(y=segment, sr=sr))
    mfcc = _safe_vector(librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=N_MFCC).mean(axis=1), N_MFCC)
    chroma = _safe_vector(librosa.feature.chroma_stft(y=segment, sr=sr).mean(axis=1), 12)

    try:
        contrast_values = librosa.feature.spectral_contrast(y=segment, sr=sr).mean(axis=1)
    except Exception:
        contrast_values = np.zeros(7, dtype=np.float64)
    spectral_contrast = _safe_vector(contrast_values, 7)

    scalar_values = [
        float(zcr),
        float(rms),
        float(tempo),
        float(onset_strength),
        float(spectral_centroid),
        float(spectral_bandwidth),
    ]
    feature_vector = scalar_values + mfcc + chroma + spectral_contrast
    feature_vector = _safe_vector(feature_vector, FEATURE_DIMENSION)

    return {
        "zcr": scalar_values[0],
        "rms": scalar_values[1],
        "tempo": scalar_values[2],
        "onset_strength": scalar_values[3],
        "spectral_centroid": scalar_values[4],
        "spectral_bandwidth": scalar_values[5],
        "mfcc": mfcc,
        "chroma": chroma,
        "spectral_contrast": spectral_contrast,
        "feature_vector": feature_vector,
    }


def extract_features(path, window_seconds=WINDOW_SECONDS, hop_seconds=HOP_SECONDS):
    y, sr = load_audio(path)
    duration = librosa.get_duration(y=y, sr=sr)
    window_samples = max(1, int(window_seconds * sr))
    hop_samples = max(1, int(hop_seconds * sr))

    if y.size < window_samples:
        starts = [0]
    else:
        starts = list(range(0, y.size - window_samples + 1, hop_samples))

    segments = []
    for segment_index, start_sample in enumerate(starts):
        end_sample = min(start_sample + window_samples, y.size)
        segment = y[start_sample:end_sample]
        if segment.size < window_samples:
            segment = np.pad(segment, (0, window_samples - segment.size))

        start_time = start_sample / sr
        end_time = min(end_sample / sr, duration)
        features = extract_segment_features(segment, sr)
        features.update({
            "segment_index": segment_index,
            "start_time": float(start_time),
            "end_time": float(end_time),
        })
        segments.append(features)

    return {
        "path": str(Path(path)),
        "duration": float(duration),
        "format": Path(path).suffix.lower().lstrip("."),
        "segments": segments,
    }


def minmax_normalize(vector, mins, maxs):
    normalized = []
    for value, min_value, max_value in zip(vector, mins, maxs):
        if math.isclose(max_value, min_value):
            normalized.append(0.0)
        else:
            normalized.append(float((value - min_value) / (max_value - min_value)))
    return normalized


def cosine_similarity(a, b):
    left = np.asarray(a, dtype=np.float64)
    right = np.asarray(b, dtype=np.float64)
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0
    return float(np.dot(left, right) / denominator)
