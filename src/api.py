from flask import Flask, request, jsonify, redirect, Response, send_from_directory
import os, time, re
from PIL import Image

from src.pipeline import load_image_bytes, compute_color_features
from src.dashboard import generate_report_html, render_gallery
from src.utils import ensure_dir, append_upload_log, get_recent_uploads

app = Flask(__name__)

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_REPORTS = os.path.join(BASE_DIR, "assets", "reports")
ASSETS_IN = os.path.join(BASE_DIR, "assets", "input")

ensure_dir(ASSETS_IN)
ensure_dir(ASSETS_REPORTS)

# health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# redirect root to dashboard
@app.route("/", methods=["GET"])
def index():
    return redirect("/dashboard", code=302)

# upload and analyze
@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return "No file uploaded. Use form field name 'file'.", 400

    file = request.files["file"]
    contents = file.read()

    try:
        img = load_image_bytes(contents)
    except Exception as e:
        return f"Invalid image: {e}", 400

    original_name = file.filename or f"upload_{int(time.time())}.jpg"
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", original_name)

    # Save original
    input_path = os.path.join(ASSETS_IN, safe_name)
    with open(input_path, "wb") as f:
        f.write(contents)

    # Compute metrics + generate detailed HTML report
    metrics = compute_color_features(img)
    report_path = generate_report_html(metrics, safe_name, out_dir=ASSETS_REPORTS)

    # Append JSON log entry
    append_upload_log({
        "filename": safe_name,
        "report_filename": os.path.basename(report_path),
        "timestamp": time.time(),
        "metrics": metrics
    })

    # Redirect to gallery
    return redirect("/dashboard", code=302)

# upload from page

@app.route("/upload", methods=["GET"])
def upload_form():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Upload Image</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">

        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Inter', sans-serif;
                background: radial-gradient(circle at top, #111827, #020617);
                color: #f3f4f6;
            }

            .upload-card {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(12px);
                border-radius: 24px;
                padding: 40px 50px;
                width: 420px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.4);
                text-align: center;
                border: 1px solid rgba(255,255,255,0.08);
                animation: fadeIn 0.6s ease-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(12px); }
                to { opacity: 1; transform: translateY(0); }
            }

            h2 {
                font-size: 26px;
                margin-bottom: 20px;
                font-weight: 600;
                color: #e5e7eb;
            }

            p {
                font-size: 14px;
                color: #9ca3af;
                margin-top: -8px;
                margin-bottom: 22px;
            }

            .dropzone {
                border: 2px dashed rgba(255,255,255,0.28);
                padding: 48px 32px;
                border-radius: 18px;

                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;

                margin: 28px auto;  /* centers within card */
                width: 100%;
                max-width: 320px;   /* makes it neat and roomy */

                transition: border-color 0.25s ease, background 0.25s ease, transform 0.2s ease;
                cursor: pointer;
            }


            .dropzone:hover {
                border-color: #60a5fa;
                background: rgba(255,255,255,0.05);
                transform: translateY(-2px);
            }


            input[type=file] {
                display: none;
            }

            button {
                width: 100%;
                padding: 14px 20px;
                margin-top: 4px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 12px;
                background: linear-gradient(to right, #3b82f6, #6366f1);
                border: none;
                color: white;
                cursor: pointer;
                transition: transform 0.2s ease, opacity 0.2s ease;
            }

            button:hover {
                opacity: 0.9;
                transform: translateY(-1px);
            }

            .link {
                margin-top: 16px;
                display: inline-block;
                font-size: 14px;
                color: #93c5fd;
                text-decoration: none;
                transition: opacity 0.2s ease;
            }

            .link:hover {
                opacity: 0.7;
            }
        </style>
    </head>

    <body>

        <div class="upload-card">
            <h2>Upload Image</h2>
            <p>Select an image to analyze its color palette</p>

            <form action="/analyze" method="POST" enctype="multipart/form-data">
                <div class="dropzone" id="dropzone">
                    <span id="drop-text">Click to choose an image<br>or drag & drop</span>
                    <input type="file" name="file" id="file-input" accept="image/*" required hidden />
                </div>
                <button type="submit">Analyze Image</button>
            </form>

            <a href="/dashboard" class="link">← Back to Dashboard</a>
        </div>

        <script>
            const dropzone = document.getElementById("dropzone");
            const fileInput = document.getElementById("file-input");
            const dropText = document.getElementById("drop-text");

            dropzone.addEventListener("click", () => fileInput.click());

            fileInput.addEventListener("change", () => {
                if (fileInput.files.length > 0) {
                    dropText.innerHTML = "✔ " + fileInput.files[0].name;
                }
            });

            dropzone.addEventListener("dragover", e => {
                e.preventDefault();
                dropzone.style.borderColor = "#60a5fa";
                dropzone.style.background = "rgba(255,255,255,0.03)";
            });

            dropzone.addEventListener("dragleave", () => {
                dropzone.style.borderColor = "rgba(255,255,255,0.25)";
                dropzone.style.background = "transparent";
            });

            dropzone.addEventListener("drop", e => {
                e.preventDefault();
                fileInput.files = e.dataTransfer.files;
                dropText.innerHTML = "✔ " + fileInput.files[0].name;
            });
        </script>

    </body>
    </html>
    """
    return html


# gallery (main dashboard)

@app.route("/dashboard", methods=["GET"])
def dashboard_index():
    uploads = get_recent_uploads(5)
    html = render_gallery(uploads)
    return Response(html, mimetype="text/html")

# static serving of input and report pages

@app.route("/input/<path:filename>")
def serve_input(filename):
    return send_from_directory(ASSETS_IN, filename)

@app.route("/dashboard/<path:filename>", methods=["GET"])
def serve_dashboard(filename):
    return send_from_directory(ASSETS_REPORTS, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
