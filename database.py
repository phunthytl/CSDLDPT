import json
import sqlite3
from pathlib import Path

DB_PATH = Path("music_search.db")


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
            format TEXT,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS track_segments (
            segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            segment_index INTEGER NOT NULL,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,
            zcr REAL NOT NULL,
            rms REAL NOT NULL,
            tempo REAL NOT NULL,
            onset_strength REAL NOT NULL,
            spectral_centroid REAL NOT NULL,
            spectral_bandwidth REAL NOT NULL,
            mfcc TEXT NOT NULL,
            chroma TEXT NOT NULL,
            spectral_contrast TEXT NOT NULL,
            feature_vector TEXT NOT NULL,
            normalized_vector TEXT,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS feature_stats (
            feature_index INTEGER PRIMARY KEY,
            min_value REAL NOT NULL,
            max_value REAL NOT NULL
        );
        """
    )
    conn.commit()


def reset_db(conn):
    conn.executescript(
        """
        DROP TABLE IF EXISTS track_segments;
        DROP TABLE IF EXISTS tracks;
        DROP TABLE IF EXISTS feature_stats;
        """
    )
    conn.commit()
    init_db(conn)


def insert_track(conn, record, extracted):
    file_path = record["local_file"]
    cursor = conn.execute(
        """
        INSERT INTO tracks (
            title, source_url, mp3_url, file_name, file_path, duration, format, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.get("title", ""),
            record.get("url", ""),
            record.get("mp3_url", ""),
            Path(file_path).name,
            file_path,
            extracted["duration"],
            extracted["format"],
            record.get("status", ""),
        ),
    )
    return cursor.lastrowid


def insert_segment(conn, track_id, segment):
    conn.execute(
        """
        INSERT INTO track_segments (
            track_id, segment_index, start_time, end_time,
            zcr, rms, tempo, onset_strength, spectral_centroid, spectral_bandwidth,
            mfcc, chroma, spectral_contrast, feature_vector, normalized_vector
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            track_id,
            segment["segment_index"],
            segment["start_time"],
            segment["end_time"],
            segment["zcr"],
            segment["rms"],
            segment["tempo"],
            segment["onset_strength"],
            segment["spectral_centroid"],
            segment["spectral_bandwidth"],
            json.dumps(segment["mfcc"]),
            json.dumps(segment["chroma"]),
            json.dumps(segment["spectral_contrast"]),
            json.dumps(segment["feature_vector"]),
            json.dumps(segment.get("normalized_vector")) if segment.get("normalized_vector") else None,
        ),
    )


def save_feature_stats(conn, mins, maxs):
    conn.execute("DELETE FROM feature_stats")
    conn.executemany(
        "INSERT INTO feature_stats (feature_index, min_value, max_value) VALUES (?, ?, ?)",
        [(index, float(min_value), float(max_value)) for index, (min_value, max_value) in enumerate(zip(mins, maxs))],
    )
    conn.commit()


def load_feature_stats(conn):
    rows = conn.execute("SELECT feature_index, min_value, max_value FROM feature_stats ORDER BY feature_index").fetchall()
    return [row["min_value"] for row in rows], [row["max_value"] for row in rows]


def load_search_segments(conn):
    rows = conn.execute(
        """
        SELECT
            s.segment_id, s.track_id, s.segment_index, s.start_time, s.end_time, s.normalized_vector,
            t.title, t.file_name, t.file_path, t.duration, t.format, t.source_url
        FROM track_segments s
        JOIN tracks t ON t.track_id = s.track_id
        WHERE s.normalized_vector IS NOT NULL
        """
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
    stats = conn.execute("SELECT COUNT(*) AS count FROM feature_stats").fetchone()["count"]
    return {"tracks": tracks, "segments": segments, "stats": stats}
