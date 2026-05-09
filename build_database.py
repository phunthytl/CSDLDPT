import json
from pathlib import Path

from audio_features import FEATURE_DIMENSION, extract_features
from database import get_connection, insert_segment, insert_track, reset_db

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
    failed = []
    total_segments = 0

    print(f"Bắt đầu build SQLite với vector {FEATURE_DIMENSION} chiều, chuẩn hóa L2...")
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
                insert_segment(conn, track_id, segment)
                total_segments += 1
            conn.commit()
            print(f"[{index}/{len(records)}] OK {path} - {len(extracted['segments'])} segments")
        except Exception as exc:
            conn.rollback()
            failed.append((path, str(exc)))
            print(f"[{index}/{len(records)}] LỖI {path}: {exc}")

    summary = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM tracks) AS tracks,
            (SELECT COUNT(*) FROM track_segments) AS segments
        """
    ).fetchone()
    conn.close()

    print("Hoàn thành build database.")
    print(f"Tracks: {summary['tracks']}")
    print(f"Segments: {summary['segments']}")
    print(f"Feature dimension: {FEATURE_DIMENSION}")
    print("Normalization: L2")
    if failed:
        print(f"File lỗi: {len(failed)}")
        for path, error in failed[:10]:
            print(f"- {path}: {error}")


if __name__ == "__main__":
    main()
