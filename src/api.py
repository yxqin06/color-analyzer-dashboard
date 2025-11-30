from flask import send_from_directory

from flask import Flask, request, jsonify, redirect
import os
import time
from PIL import Image

from src.pipeline import load_image_bytes, compute_color_features
from src.dashboard import generate_report_html

from src.utils import ensure_dir

app = Flask(__name__)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_REPORTS = os.path.join(BASE_DIR, "assets", "reports")
ASSETS_IN = os.path.join(BASE_DIR, "assets", "input")

#ASSETS_IN = "assets/input"
#ASSETS_REPORTS = "../assets/reports"

ensure_dir(ASSETS_IN)
ensure_dir(ASSETS_REPORTS)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

"""
@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use form field name 'file'."}), 400

    file = request.files["file"]
    contents = file.read()

    try:
        img = load_image_bytes(contents)
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    original_name = file.filename or f"upload_{int(time.time())}.jpg"
    safe_name = original_name.replace(" ", "_")
    input_path = os.path.join(ASSETS_IN, safe_name)

    with open(input_path, "wb") as f:
        f.write(contents)

    metrics = compute_color_features(img)
    report_path = generate_report_html(metrics, safe_name, out_dir=ASSETS_REPORTS)

    output = metrics.copy()
    output["dashboard_url"] = f"http://127.0.0.1:5000/dashboard/{os.path.basename(report_path)}"

    return jsonify(output)
"""
@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use form field name 'file'."}), 400

    file = request.files["file"]
    contents = file.read()

    try:
        img = load_image_bytes(contents)
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    original_name = file.filename or f"upload_{int(time.time())}.jpg"
    safe_name = original_name.replace(" ", "_")
    input_path = os.path.join(ASSETS_IN, safe_name)

    with open(input_path, "wb") as f:
        f.write(contents)

    metrics = compute_color_features(img)
    report_path = generate_report_html(metrics, safe_name, out_dir=ASSETS_REPORTS)

    # NEW: Direct redirect to the dashboard
    return redirect(f"/dashboard/{os.path.basename(report_path)}", code=302)

@app.route("/upload", methods=["GET"])
def upload_form():
    html = """
    <html>
    <head>
        <title>Upload Image</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 30px;
            }
            .container {
                max-width: 400px;
                margin: 0 auto;
                padding: 25px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            input[type=file] {
                margin-top: 15px;
                margin-bottom: 15px;
            }
            button {
                padding: 10px 20px;
                background: #0077cc;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #005fa3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Upload Image for Analysis</h2>
            <form action="/analyze" method="POST" enctype="multipart/form-data">
                <input type="file" name="file" required><br>
                <button type="submit">Analyze</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

@app.route("/input/<path:filename>")
def serve_input(filename):
    return send_from_directory(ASSETS_IN, filename)

@app.route("/dashboard/<path:filename>", methods=["GET"])
def serve_dashboard(filename):
    return send_from_directory(ASSETS_REPORTS, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
