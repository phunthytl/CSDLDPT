from pathlib import Path

import librosa
import numpy as np
import soundfile

TARGET_SAMPLE_RATE = 22050
WINDOW_SECONDS = 5.0
HOP_SECONDS = 2.5
N_MFCC = 13
N_CHROMA = 12
N_CONTRAST = 7
FEATURE_DIMENSION = 78

FEATURE_NAMES = [
    "Tempo",
    "OnsetMean",
    "OnsetStd",
    "OnsetDensity",
    "RMSMean",
    "RMSStd",
    "ZCRMean",
    "ZCRStd",
    "SpectralCentroidMean",
    "SpectralCentroidStd",
    "SpectralBandwidthMean",
    "SpectralBandwidthStd",
    "SpectralRolloffMean",
    "SpectralRolloffStd",
    *[f"SpectralContrastMean_{i}" for i in range(1, N_CONTRAST + 1)],
    *[f"SpectralContrastStd_{i}" for i in range(1, N_CONTRAST + 1)],
    *[f"MFCCMean_{i}" for i in range(1, N_MFCC + 1)],
    *[f"MFCCStd_{i}" for i in range(1, N_MFCC + 1)],
    *[f"ChromaMean_{i}" for i in range(1, N_CHROMA + 1)],
    *[f"ChromaStd_{i}" for i in range(1, N_CHROMA + 1)],
]

if len(FEATURE_NAMES) != FEATURE_DIMENSION:
    raise RuntimeError(f"FEATURE_NAMES has {len(FEATURE_NAMES)} names, expected {FEATURE_DIMENSION}")


def load_audio(path):
    y, sr = soundfile.read(path, dtype="float32", always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if sr > TARGET_SAMPLE_RATE:
        step = max(1, round(sr / TARGET_SAMPLE_RATE))
        y = y[::step]
        sr = round(sr / step)
    return y.astype(np.float32), sr


def clean_array(values):
    arr = np.asarray(values, dtype=np.float64)
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)


def mean_std(values):
    arr = clean_array(values)
    if arr.size == 0:
        return 0.0, 0.0
    return float(arr.mean()), float(arr.std())


def row_mean_std(matrix, rows):
    arr = clean_array(matrix)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.shape[0] < rows:
        arr = np.pad(arr, ((0, rows - arr.shape[0]), (0, 0)))
    arr = arr[:rows]
    means = arr.mean(axis=1)
    stds = arr.std(axis=1)
    return means.astype(float).tolist(), stds.astype(float).tolist()


def estimate_tempo(onset_env, sr):
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="frames")
    if onset_frames.size <= 1:
        return 0.0, 0.0
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    intervals = np.diff(onset_times)
    intervals = intervals[intervals > 0]
    if intervals.size == 0:
        return 0.0, float(onset_frames.size)
    tempo = 60.0 / np.median(intervals)
    return float(tempo), float(onset_frames.size)


def l2_normalize(vector):
    arr = clean_array(vector).reshape(-1)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr.astype(float).tolist()
    return (arr / norm).astype(float).tolist()


def extract_segment_features(segment, sr):
    if segment.size == 0:
        raise ValueError("Empty audio segment")

    duration = segment.size / sr

    zcr_mean, zcr_std = mean_std(librosa.feature.zero_crossing_rate(y=segment))
    rms_mean, rms_std = mean_std(librosa.feature.rms(y=segment))

    onset_env = librosa.onset.onset_strength(y=segment, sr=sr)
    onset_mean, onset_std = mean_std(onset_env)
    tempo, onset_count = estimate_tempo(onset_env, sr)
    onset_density = float(onset_count / duration) if duration > 0 else 0.0

    centroid_mean, centroid_std = mean_std(librosa.feature.spectral_centroid(y=segment, sr=sr))
    bandwidth_mean, bandwidth_std = mean_std(librosa.feature.spectral_bandwidth(y=segment, sr=sr))
    rolloff_mean, rolloff_std = mean_std(librosa.feature.spectral_rolloff(y=segment, sr=sr, roll_percent=0.85))

    try:
        contrast = librosa.feature.spectral_contrast(y=segment, sr=sr, n_bands=6)
    except Exception:
        contrast = np.zeros((N_CONTRAST, 1), dtype=np.float64)
    contrast_mean, contrast_std = row_mean_std(contrast, N_CONTRAST)

    mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=N_MFCC)
    mfcc_mean, mfcc_std = row_mean_std(mfcc, N_MFCC)

    chroma = librosa.feature.chroma_stft(y=segment, sr=sr, n_chroma=N_CHROMA)
    chroma_mean, chroma_std = row_mean_std(chroma, N_CHROMA)

    tempo = float(tempo)
    onset_mean = float(onset_mean)
    onset_std = float(onset_std)
    onset_density = float(onset_density)
    rms_mean = float(rms_mean)
    rms_std = float(rms_std)
    zcr_mean = float(zcr_mean)
    zcr_std = float(zcr_std)
    centroid_mean = float(centroid_mean)
    centroid_std = float(centroid_std)
    bandwidth_mean = float(bandwidth_mean)
    bandwidth_std = float(bandwidth_std)
    rolloff_mean = float(rolloff_mean)
    rolloff_std = float(rolloff_std)

    feature_vector = [
        tempo,
        onset_mean,
        onset_std,
        onset_density,
        rms_mean,
        rms_std,
        zcr_mean,
        zcr_std,
        centroid_mean,
        centroid_std,
        bandwidth_mean,
        bandwidth_std,
        rolloff_mean,
        rolloff_std,
        *contrast_mean,
        *contrast_std,
        *mfcc_mean,
        *mfcc_std,
        *chroma_mean,
        *chroma_std,
    ]
    feature_vector = clean_array(feature_vector).astype(float).tolist()
    if len(feature_vector) != FEATURE_DIMENSION:
        raise ValueError(f"Feature vector has {len(feature_vector)} dimensions, expected {FEATURE_DIMENSION}")

    return {
        "tempo": float(tempo),
        "onset_mean": float(onset_mean),
        "onset_std": float(onset_std),
        "onset_density": float(onset_density),
        "rms_mean": float(rms_mean),
        "rms_std": float(rms_std),
        "zcr_mean": float(zcr_mean),
        "zcr_std": float(zcr_std),
        "spectral_centroid_mean": float(centroid_mean),
        "spectral_centroid_std": float(centroid_std),
        "spectral_bandwidth_mean": float(bandwidth_mean),
        "spectral_bandwidth_std": float(bandwidth_std),
        "spectral_rolloff_mean": float(rolloff_mean),
        "spectral_rolloff_std": float(rolloff_std),
        "spectral_contrast_mean": contrast_mean,
        "spectral_contrast_std": contrast_std,
        "mfcc_mean": mfcc_mean,
        "mfcc_std": mfcc_std,
        "chroma_mean": chroma_mean,
        "chroma_std": chroma_std,
        "feature_vector": feature_vector,
        "normalized_vector": l2_normalize(feature_vector),
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

        features = extract_segment_features(segment, sr)
        features.update({
            "segment_index": segment_index,
            "start_time": float(start_sample / sr),
            "end_time": float(min(end_sample / sr, duration)),
        })
        segments.append(features)

    return {
        "path": str(Path(path)),
        "duration": float(duration),
        "format": Path(path).suffix.lower().lstrip("."),
        "segments": segments,
    }


def cosine_similarity(a, b):
    left = clean_array(a).reshape(-1)
    right = clean_array(b).reshape(-1)
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0
    return float(np.dot(left, right) / denominator)
