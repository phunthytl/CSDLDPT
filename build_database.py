import json
from pathlib import Path

import numpy as np

from audio_features import FEATURE_DIMENSION, extract_features, l2_normalize
from database import get_connection, insert_segment, insert_track, reset_db, save_feature_stats

METADATA_PATH = Path("pixabay_music.json")


def load_records():
    with METADATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def collect_valid_records(records):
    valid = []
    for record in records:
        local_file = record.get("local_file")
        if local_file and Path(local_file).exists():
            valid.append(record)
    return valid


def zscore_vector(vector, mean_vector, std_vector):
    vector = np.asarray(vector, dtype=np.float64)
    mean_vector = np.asarray(mean_vector, dtype=np.float64)
    std_vector = np.asarray(std_vector, dtype=np.float64)
    safe_std = np.where(std_vector == 0, 1.0, std_vector)
    return ((vector - mean_vector) / safe_std).astype(float).tolist()


def main():
    records = collect_valid_records(load_records())
    if not records:
        raise SystemExit("Không tìm thấy file âm thanh hợp lệ từ pixabay_music.json")

    conn = get_connection()
    reset_db(conn)
    failed = []
    all_vectors = []
    total_segments = 0

    print(f"Bắt đầu build SQLite với vector thô {FEATURE_DIMENSION} chiều...")
    print(f"Số file hợp lệ: {len(records)}")

    for index, record in enumerate(records, start=1):
        path = record["local_file"]
        try:
            extracted = extract_features(path)
            track_id = insert_track(conn, record, extracted)
            for segment in extracted["segments"]:
                if len(segment["feature_vector"]) != FEATURE_DIMENSION:
                    raise ValueError(
                        f"Sai số chiều vector: {len(segment['feature_vector'])} != {FEATURE_DIMENSION}"
                    )
                all_vectors.append(segment["feature_vector"])
                insert_segment(conn, track_id, segment)
                total_segments += 1
            conn.commit()
            print(f"[{index}/{len(records)}] OK {path} - {len(extracted['segments'])} segments")
        except Exception as exc:
            conn.rollback()
            failed.append((path, str(exc)))
            print(f"[{index}/{len(records)}] LỖI {path}: {exc}")

    if not all_vectors:
        conn.close()
        raise SystemExit("Không trích xuất được segment hợp lệ nào.")

    print("Đang tính mean/std và cập nhật normalized_vector = L2(Z-score(vector))...")
    vector_matrix = np.asarray(all_vectors, dtype=np.float64)
    mean_vector = vector_matrix.mean(axis=0).astype(float).tolist()
    std_vector = vector_matrix.std(axis=0).astype(float).tolist()
    save_feature_stats(conn, mean_vector, std_vector)

    rows = conn.execute("SELECT segment_id, feature_vector FROM track_segments").fetchall()
    for row in rows:
        vector = json.loads(row["feature_vector"])
        z_vector = zscore_vector(vector, mean_vector, std_vector)
        normalized = l2_normalize(z_vector)
        conn.execute(
            "UPDATE track_segments SET normalized_vector = ? WHERE segment_id = ?",
            (json.dumps(normalized), row["segment_id"]),
        )
    conn.commit()

    summary = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM tracks) AS tracks,
            (SELECT COUNT(*) FROM track_segments) AS segments,
            (SELECT COUNT(*) FROM track_segments WHERE normalized_vector IS NOT NULL) AS ready_segments
        """
    ).fetchone()
    conn.close()

    print("Hoàn thành build database.")
    print(f"Tracks: {summary['tracks']}")
    print(f"Segments: {summary['segments']}")
    print(f"Ready segments: {summary['ready_segments']}")
    print(f"Feature dimension: {FEATURE_DIMENSION}")
    print("Normalization: Z-score + L2")
    if failed:
        print(f"File lỗi: {len(failed)}")
        for path, error in failed[:10]:
            print(f"- {path}: {error}")


if __name__ == "__main__":
    main()
