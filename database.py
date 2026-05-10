import json
import sqlite3
from pathlib import Path

DB_PATH = Path("musics.db")
FEATURE_STATS_KEY = "zscore"


def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source_url TEXT,
            mp3_url TEXT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL UNIQUE,
            duration REAL,
            format TEXT
        );

        CREATE TABLE IF NOT EXISTS track_segments (
            segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            segment_index INTEGER NOT NULL,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,

            tempo REAL NOT NULL,
            onset_mean REAL NOT NULL,
            onset_std REAL NOT NULL,
            onset_density REAL NOT NULL,

            rms_mean REAL NOT NULL,
            rms_std REAL NOT NULL,
            zcr_mean REAL NOT NULL,
            zcr_std REAL NOT NULL,

            spectral_centroid_mean REAL NOT NULL,
            spectral_centroid_std REAL NOT NULL,
            spectral_bandwidth_mean REAL NOT NULL,
            spectral_bandwidth_std REAL NOT NULL,
            spectral_rolloff_mean REAL NOT NULL,
            spectral_rolloff_std REAL NOT NULL,

            spectral_contrast_mean TEXT NOT NULL,
            spectral_contrast_std TEXT NOT NULL,
            mfcc_mean TEXT NOT NULL,
            mfcc_std TEXT NOT NULL,
            chroma_mean TEXT NOT NULL,
            chroma_std TEXT NOT NULL,
            feature_vector TEXT NOT NULL,
            normalized_vector TEXT,

            FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS feature_stats (
            stats_key TEXT PRIMARY KEY,
            mean_vector TEXT NOT NULL,
            std_vector TEXT NOT NULL
        );
        """
    )
    conn.commit()


def reset_db(conn):
    conn.executescript(
        """
        DROP TABLE IF EXISTS feature_stats;
        DROP TABLE IF EXISTS track_segments;
        DROP TABLE IF EXISTS tracks;
        """
    )
    conn.commit()
    init_db(conn)


def insert_track(conn, record, extracted):
    file_path = record["local_file"]
    cursor = conn.execute(
        """
        INSERT INTO tracks (
            title, source_url, mp3_url, file_name, file_path, duration, format
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.get("title", ""),
            record.get("url", ""),
            record.get("mp3_url", ""),
            Path(file_path).name,
            file_path,
            extracted["duration"],
            extracted["format"],
        ),
    )
    return cursor.lastrowid


def insert_segment(conn, track_id, segment):
    vector = segment["feature_vector"]
    normalized = segment["normalized_vector"]

    conn.execute(
        """
        INSERT INTO track_segments (
            track_id, segment_index, start_time, end_time,
            tempo, onset_mean, onset_std, onset_density,
            rms_mean, rms_std, zcr_mean, zcr_std,
            spectral_centroid_mean, spectral_centroid_std,
            spectral_bandwidth_mean, spectral_bandwidth_std,
            spectral_rolloff_mean, spectral_rolloff_std,
            spectral_contrast_mean, spectral_contrast_std,
            mfcc_mean, mfcc_std, chroma_mean, chroma_std,
            feature_vector, normalized_vector
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            track_id,
            segment["segment_index"],
            segment["start_time"],
            segment["end_time"],
            segment["tempo"],
            segment["onset_mean"],
            segment["onset_std"],
            segment["onset_density"],
            segment["rms_mean"],
            segment["rms_std"],
            segment["zcr_mean"],
            segment["zcr_std"],
            segment["spectral_centroid_mean"],
            segment["spectral_centroid_std"],
            segment["spectral_bandwidth_mean"],
            segment["spectral_bandwidth_std"],
            segment["spectral_rolloff_mean"],
            segment["spectral_rolloff_std"],
            json.dumps(segment["spectral_contrast_mean"]),
            json.dumps(segment["spectral_contrast_std"]),
            json.dumps(segment["mfcc_mean"]),
            json.dumps(segment["mfcc_std"]),
            json.dumps(segment["chroma_mean"]),
            json.dumps(segment["chroma_std"]),
            json.dumps(vector),
            json.dumps(normalized),
        ),
    )


def save_feature_stats(conn, mean_vector, std_vector):
    conn.execute(
        """
        INSERT INTO feature_stats (stats_key, mean_vector, std_vector)
        VALUES (?, ?, ?)
        ON CONFLICT(stats_key) DO UPDATE SET
            mean_vector = excluded.mean_vector,
            std_vector = excluded.std_vector
        """,
        (FEATURE_STATS_KEY, json.dumps(mean_vector), json.dumps(std_vector)),
    )


def load_feature_stats(conn):
    row = conn.execute(
        "SELECT mean_vector, std_vector FROM feature_stats WHERE stats_key = ?",
        (FEATURE_STATS_KEY,),
    ).fetchone()
    if row is None:
        return None
    return {
        "mean_vector": json.loads(row["mean_vector"]),
        "std_vector": json.loads(row["std_vector"]),
    }


def load_search_segments(conn):
    rows = conn.execute(
        """
        SELECT
            s.segment_id, s.track_id, s.segment_index, s.start_time, s.end_time, s.normalized_vector,
            t.title, t.file_name, t.file_path, t.duration, t.format, t.source_url
        FROM track_segments s
        JOIN tracks t ON t.track_id = s.track_id
        WHERE s.normalized_vector IS NOT NULL
        """,
    ).fetchall()

    segments = []
    for row in rows:
        item = dict(row)
        item["normalized_vector"] = json.loads(item["normalized_vector"])
        segments.append(item)
    return segments


def database_summary(conn):
    tracks = conn.execute("SELECT COUNT(*) AS count FROM tracks").fetchone()["count"]
    segments = conn.execute("SELECT COUNT(*) AS count FROM track_segments").fetchone()["count"]
    ready_segments = conn.execute(
        "SELECT COUNT(*) AS count FROM track_segments WHERE normalized_vector IS NOT NULL"
    ).fetchone()["count"]
    return {
        "tracks": tracks,
        "segments": segments,
        "ready_segments": ready_segments,
        "feature_dimension": 78,
        "normalization": "Z-score + L2",
    }
