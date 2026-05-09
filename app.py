from collections import defaultdict
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from audio_features import cosine_similarity, extract_features
from database import database_summary, get_connection, load_search_segments

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "flac", "aac", "webm"}
UPLOAD_FOLDER = Path("uploads")
MUSIC_FOLDER = Path("musics")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_state():
    try:
        with get_connection() as conn:
            return database_summary(conn)
    except Exception:
        return {"tracks": 0, "segments": 0, "stats": 0}


def aggregate_results(query_segments, db_segments):
    track_scores = defaultdict(list)
    track_best_matches = {}

    for query_segment in query_segments:
        best_by_track = {}
        for db_segment in db_segments:
            score = cosine_similarity(query_segment["normalized_vector"], db_segment["normalized_vector"])
            track_id = db_segment["track_id"]
            current = best_by_track.get(track_id)
            if current is None or score > current["score"]:
                best_by_track[track_id] = {
                    "score": score,
                    "query_segment": query_segment,
                    "db_segment": db_segment,
                }

        for track_id, match in best_by_track.items():
            track_scores[track_id].append(match["score"])
            current = track_best_matches.get(track_id)
            if current is None or match["score"] > current["score"]:
                track_best_matches[track_id] = match

    results = []
    for track_id, scores in track_scores.items():
        best_match = track_best_matches[track_id]
        query_segment = best_match["query_segment"]
        db_segment = best_match["db_segment"]
        results.append(
            {
                "track_id": track_id,
                "title": db_segment["title"],
                "file_name": db_segment["file_name"],
                "file_path": db_segment["file_path"],
                "duration": db_segment["duration"],
                "format": db_segment["format"],
                "source_url": db_segment["source_url"],
                "score": sum(scores) / len(scores),
                "best_pair_score": best_match["score"],
                "query_segment_index": query_segment["segment_index"],
                "query_segment_start": query_segment["start_time"],
                "query_segment_end": query_segment["end_time"],
                "db_segment_index": db_segment["segment_index"],
                "db_segment_start": db_segment["start_time"],
                "db_segment_end": db_segment["end_time"],
                "audio_url": url_for("audio_file", filename=Path(db_segment["file_path"]).name),
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)[:5]


@app.route("/")
def index():
    return render_template("index.html", summary=get_db_state())


@app.route("/search", methods=["POST"])
def search():
    upload = request.files.get("audio_file")
    if not upload or upload.filename == "":
        return render_template("index.html", summary=get_db_state(), error="Vui lòng chọn file âm thanh.")
    if not allowed_file(upload.filename):
        return render_template("index.html", summary=get_db_state(), error="Định dạng file không được hỗ trợ.")

    original_name = secure_filename(upload.filename)
    saved_name = f"{uuid4().hex}_{original_name}"
    upload_path = UPLOAD_FOLDER / saved_name
    upload.save(upload_path)

    try:
        with get_connection() as conn:
            db_segments = load_search_segments(conn)
            summary = database_summary(conn)

        if not db_segments:
            return render_template(
                "index.html",
                summary=summary,
                error="Database chưa sẵn sàng. Hãy chạy lại: python build_database.py",
            )

        extracted = extract_features(upload_path)
        query_segments = extracted["segments"]

        results = aggregate_results(query_segments, db_segments)
        intermediate = {
            "query_segments": len(query_segments),
            "db_segments": len(db_segments),
            "tracks": summary["tracks"],
            "duration": extracted["duration"],
            "feature_dimension": summary["feature_dimension"],
            "normalization": summary["normalization"],
        }

        return render_template(
            "results.html",
            query_name=original_name,
            query_url=url_for("uploaded_file", filename=saved_name),
            results=results,
            intermediate=intermediate,
            summary=summary,
        )
    except Exception as exc:
        return render_template("index.html", summary=get_db_state(), error=f"Không xử lý được file: {exc}")


@app.route("/audio/<path:filename>")
def audio_file(filename):
    path = MUSIC_FOLDER / filename
    if not path.exists():
        abort(404)
    return send_from_directory(MUSIC_FOLDER, filename)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    path = UPLOAD_FOLDER / filename
    if not path.exists():
        abort(404)
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
