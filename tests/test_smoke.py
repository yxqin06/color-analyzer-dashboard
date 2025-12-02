import os
import json
from src.api import app

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_dashboard_loads():
    client = app.test_client()
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert b"Recent" in res.data or b"Upload" in res.data

def test_upload_log_file_exists():
    from src.utils import UPLOAD_LOG
    # ensure directory exists
    os.makedirs(os.path.dirname(UPLOAD_LOG), exist_ok=True)
    # write dummy entry
    with open(UPLOAD_LOG, "w") as f:
        json.dump([], f)
    assert os.path.exists(UPLOAD_LOG)
