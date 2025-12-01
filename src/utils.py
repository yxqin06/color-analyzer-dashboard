import os
import json
import time

# Base directory: project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory & log file
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_LOG = os.path.join(DATA_DIR, "uploads.json")


def ensure_dir(path: str):
    # Create directory if it does not exist.
    os.makedirs(path, exist_ok=True)


def load_upload_log(path: str = UPLOAD_LOG) -> list:
    # Load uploads.json if it exists, else return an empty list.
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # fallback if file corrupted


def append_upload_log(entry: dict, path: str = UPLOAD_LOG) -> None:
    # Append a new log entry and save the JSON file.
    ensure_dir(os.path.dirname(path))  # ensure /data/ exists
    log = load_upload_log(path)
    log.append(entry) 

    with open(path, "w") as f:
        json.dump(log, f, indent=2)


def get_recent_uploads(n: int = 5, path: str = UPLOAD_LOG) -> list:
    # Return last n uploads sorted by timestamp descending.
    log = load_upload_log(path)
    log = sorted(log, key=lambda e: e.get("timestamp", 0), reverse=True)
    return log[:n]
