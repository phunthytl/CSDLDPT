import json
from pathlib import Path

import numpy as np

from audio_features import FEATURE_DIMENSION, extract_features, minmax_normalize
from database import get_connection, init_db, insert_segment, insert_track, reset_db, save_feature_stats

METADATA_PATH = Path("pixabay_music.json")


def load_records():
    with METADATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def collect_valid_records(records):
    valid = []
    for record in records:
        local_file = record.get("local_file")
        if record.get("status") == "ok" and local_file and Path(local_file).exists():
            valid.append(record)
    return valid


def main():
    records = collect_valid_records(load_records())
    if not records:
        raise SystemExit("Không tìm thấy file âm thanh hợp lệ từ pixabay_music.json")

    conn = get_connection()
    reset_db(conn)

    pending_segments = []
    failed = []

    print(f"Bắt đầu trích xuất {len(records)} file âm thanh...")
    for index, record in enumerate(records, start=1):
        path = record["local_file"]
        try:
            extracted = extract_features(path)
            track_id = insert_track(conn, record, extracted)
            for segment in extracted["segments"]:
                pending_segments.append((track_id, segment))
            conn.commit()
            print(f"[{index}/{len(records)}] OK {path} - {len(extracted['segments'])} segments")
        except Exception as exc:
            conn.rollback()
            failed.append((path, str(exc)))
            print(f"[{index}/{len(records)}] LỖI {path}: {exc}")

    if not pending_segments:
        raise SystemExit("Không trích xuất được segment nào")

    vectors = np.asarray([segment["feature_vector"] for _, segment in pending_segments], dtype=np.float64)
    if vectors.shape[1] != FEATURE_DIMENSION:
        raise SystemExit(f"Sai số chiều vector: {vectors.shape[1]} != {FEATURE_DIMENSION}")

    mins = vectors.min(axis=0).tolist()
    maxs = vectors.max(axis=0).tolist()
    save_feature_stats(conn, mins, maxs)

    print("Đang lưu segment đã chuẩn hóa vào SQLite...")
    for track_id, segment in pending_segments:
        segment["normalized_vector"] = minmax_normalize(segment["feature_vector"], mins, maxs)
        insert_segment(conn, track_id, segment)
    conn.commit()

    summary = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM tracks) AS tracks,
            (SELECT COUNT(*) FROM track_segments) AS segments,
            (SELECT COUNT(*) FROM feature_stats) AS stats
        """
    ).fetchone()
    conn.close()

    print("Hoàn thành build database.")
    print(f"Tracks: {summary['tracks']}")
    print(f"Segments: {summary['segments']}")
    print(f"Feature stats: {summary['stats']}")
    if failed:
        print(f"File lỗi: {len(failed)}")
        for path, error in failed[:10]:
            print(f"- {path}: {error}")


if __name__ == "__main__":
    init_db(get_connection())
    main()
