import os
from jinja2 import Template
from src.utils import ensure_dir

# GALLERY TEMPLATE
GALLERY_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Recent Color Analyses</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/satoshi/latin.css">



  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

        .empty-state {
        margin-top: 80px;
        text-align: center;
        animation: fadeIn 0.6s ease-out;
    }

    .empty-title {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 12px;
        color: #e5e7eb;
    }

    .empty-subtitle {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 26px;
    }

    .empty-btn {
        padding: 14px 26px;
        background: linear-gradient(to right, #3b82f6, #6366f1);
        border-radius: 999px;
        font-size: 16px;
        font-weight: 600;
        color: white;
        text-decoration: none;
        transition: opacity 0.2s ease, transform 0.2s ease;
    }

    .empty-btn:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }


    body {
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at top, #111827, #020617);
      color: #f9fafb;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px 16px 60px;
    }

    h1 {
        font-size: 46px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        text-align: center;
        margin-bottom: 22px;

        background: linear-gradient(to right, #ffffff, #d1d5db, #9ca3af);
        -webkit-background-clip: text;
        color: transparent;

        text-shadow: 0 0 18px rgba(255,255,255,0.07);
        opacity: 0;
        animation: cinematicFade 0.9s ease-out forwards;
    }

    @keyframes cinematicFade {
        0% {
            opacity: 0;
            transform: translateY(14px) scale(0.98);
            letter-spacing: 0.25em;
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
            letter-spacing: 0.12em;
        }
    }

        h2 {
        font-family: 'Satoshi', sans-serif;
        letter-spacing: 0.03em; 
        font-weight: 600; 
    }




    .upload-btn {
        position: absolute;
        top: 20px;
        right: 25px;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        padding: 10px 18px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        text-decoration: none;
        font-size: 14px;
        box-shadow: 0 6px 18px rgba(99,102,241,0.45);
        transition: transform 0.15s ease, box-shadow 0.3s ease;
    }

    .upload-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99,102,241,0.6);
        opacity: 0.95;
    }


    .subtitle {
      font-size: 14px;
      color: #9ca3af;
      margin-bottom: 26px;
      text-align: center;
    }

    /* Container */
    .cont {
      position: relative;
      max-width: 1080px;
      width: 100%;
      height: 420px;
      overflow: hidden;
      border-radius: 26px;
      background: rgba(15,23,42,0.9);
      box-shadow: 0 24px 60px rgba(0,0,0,0.4);
      display: flex;
      align-items: stretch;
      justify-content: stretch;
      transition: opacity 0.7s ease, transform 0.7s ease;
    }

    .cont.s--inactive {
      opacity: 0;
      transform: translateY(12px);
    }

    .cont__inner {
      position: relative;
      display: flex;
      width: 100%;
      height: 100%;
    }

    /* Element (panel) */
    .el {
      position: relative;
      flex: 1;
      cursor: pointer;
      overflow: hidden;
      transition: flex 0.6s ease, transform 0.6s ease;
      transform-origin: center;
      border-right: 1px solid rgba(148,163,184,0.15);
    }

    .el:last-child { border-right: none; }

    .el__overflow {
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    .el__inner {
      position: relative;
      width: 100%;
      height: 100%;
      padding: 20px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.6s ease;
    }

    .el__bg {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at top, rgba(148,163,253,0.2), transparent 60%),
                  radial-gradient(circle at bottom, rgba(248,250,252,0.06), transparent 60%);
      opacity: 0.2;
      transition: opacity 0.6s ease;
      z-index: -1;
    }

    .el__preview-cont {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .el__heading {
      font-size: 18px;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #e5e7eb;
    }

    .el__thumb {
      width: 100%;
      border-radius: 18px;
      overflow: hidden;
      background: #020617;
      border: 1px solid rgba(148,163,184,0.25);
      position: relative;
    }

    .el__thumb img {
      width: 100%;
      height: 130px;
      object-fit: cover;
      filter: saturate(1.05);
      transition: transform 0.5s ease;
    }

    .el__thumb-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(15,23,42,0.8), transparent 80%);
      pointer-events: none;
    }

    .el__tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
      font-size: 11px;
    }

    .badge {
      padding: 4px 9px;
      border-radius: 999px;
      font-weight: 500;
      text-transform: uppercase;
      font-size: 10px;
    }

    .warm { background: rgba(248, 181, 129, 0.18); color: #fed7aa; border: 1px solid rgba(248, 181, 129, 0.5); }
    .cool { background: rgba(129, 199, 248, 0.18); color: #bae6fd; border: 1px solid rgba(129, 199, 248, 0.5); }
    .light { background: rgba(254, 240, 138, 0.16); color: #fef9c3; border: 1px solid rgba(254, 240, 138, 0.45); }
    .dark  { background: rgba(148,163,184,0.16); color: #e5e7eb; border: 1px solid rgba(148,163,184,0.45); }

    /* Expanded panel */
    .el__content {
      position: absolute;
      inset: 0;
      padding: 22px 22px 26px;
      background: radial-gradient(circle at top left, rgba(129,140,248,0.16), transparent 55%),
                  radial-gradient(circle at bottom right, rgba(15,23,42,0.96), #020617);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.5s ease;
      display: flex;
      flex-direction: column;
    }

    .el--active .el__content {
      opacity: 1;
      pointer-events: auto;
    }

    .el__content-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .el__content-title {
      font-size: 20px;
      font-weight: 600;
    }

    .el__close-btn {
      width: 26px;
      height: 26px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      cursor: pointer;
      background: rgba(15,23,42,0.9);
    }

    .el__close-btn::before { content: "×"; }

    .el__content-body {
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 20px;
      flex: 1;
    }

    .section-block-title {
      font-size: 13px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #9ca3af;
      margin-bottom: 10px;
    }

    .main-color-swatch {
      width: 100%;
      height: 120px;
      border-radius: 18px;
      border: 1px solid rgba(148,163,184,0.4);
      margin-bottom: 10px;
    }

    .palette-row {
      display: flex;
      gap: 8px;
    }

    .palette-swatch {
      flex: 1;
      height: 42px;
      border-radius: 999px;
      border: 1px solid rgba(15,23,42,0.9);
    }

    .metric-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .metric-table tr + tr td {
      border-top: 1px solid rgba(31,41,55,0.9);
    }

    .metric-table td {
      padding: 6px 0;
    }

    .metric-label { color: #9ca3af; width: 120px; }
    .metric-value { font-weight: 500; color: #e5e7eb; }

    .el__index {
      position: absolute;
      bottom: 12px;
      left: 16px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: rgba(148,163,184,0.8);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .el__index-front {
      padding: 3px 9px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,0.6);
      background: rgba(15,23,42,0.9);
      font-size: 10px;
      cursor: pointer;
    }

    .el--active {
      flex: 3.4;
      z-index: 2;
    }

    .el--active .el__thumb img {
      transform: scale(1.04);
    }

    .el--active .el__bg {
      opacity: 0.55;
    }

    .cont.s--active .el:not(.el--active) {
      transform: scale(0.98);
      opacity: 0.9;
    }

    .empty-state {
      text-align: center;
      color: #9ca3af;
      font-size: 14px;
      margin-top: 40px;
    }

    @media (max-width: 900px) {
      .cont { height: 540px; }
      .el__content-body { grid-template-columns: 1fr; }
    }

    @media (max-width: 640px) {
      .cont { height: 580px; }
    }
  </style>
</head>

<body>
  <a class="upload-btn" href="/upload">⬆️ Upload Image</a>
  <h1>Color Analysis</h1>
  <div class="subtitle">
    Latest {{ uploads|length }} uploads, with palettes, classification, and metrics.
  </div>

  {% if uploads %}
  <div class="cont s--inactive">
    <div class="cont__inner">

      {% for upload in uploads %}
      {% set m = upload.metrics %}
      <div class="el" data-index="{{ loop.index0 }}">
        <div class="el__overflow">
          <div class="el__inner">
            <div class="el__bg"></div>

            <div class="el__preview-cont">
              <h2 class="el__heading">Upload {{ loop.index }}</h2>

              <div class="el__thumb">
                <img src="/input/{{ upload.filename }}">
                <div class="el__thumb-overlay"></div>
              </div>

              <div class="el__tags">
                <span class="badge {{ m.temperature }}">{{ m.temperature|capitalize }}</span>
                <span class="badge {{ m.brightness }}">{{ m.brightness|capitalize }}</span>
              </div>
            </div>

            <div class="el__content">
              <div class="el__content-header">
                <div class="el__content-title">Upload {{ loop.index }} Details</div>
                <div class="el__close-btn"></div>
              </div>

              <div class="el__content-body">
                <div>
                  <div class="section-block-title">Main Color & Palette</div>

                  <div class="main-color-swatch" 
                       style="background-color: rgb({{ m.main_color[0] }}, {{ m.main_color[1] }}, {{ m.main_color[2] }});">
                  </div>

                  <div class="palette-row">
                    {% for c in m.dominant_colors %}
                    <div class="palette-swatch"
                         style="background-color: rgb({{ c[0] }}, {{ c[1] }}, {{ c[2] }});">
                    </div>
                    {% endfor %}
                  </div>

                  <a class="view-report-link" href="/dashboard/{{ upload.report_filename }}" target="_blank">
                    Full report ↗
                  </a>
                </div>

                <div>
                  <div class="section-block-title">Metrics</div>

                  <table class="metric-table">
                    <tr>
                      <td class="metric-label">Hue</td>
                      <td class="metric-value">{{ m.hue | round(2) }}</td>
                    </tr>
                    <tr>
                      <td class="metric-label">Saturation</td>
                      <td class="metric-value">{{ m.saturation | round(3) }}</td>
                    </tr>
                    <tr>
                      <td class="metric-label">Value</td>
                      <td class="metric-value">{{ m.value | round(3) }}</td>
                    </tr>
                    <tr>
                      <td class="metric-label">Luminance</td>
                      <td class="metric-value">{{ m.luminance | round(3) }}</td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>

          </div>
        </div>

        <div class="el__index">
          <div>{{ loop.index }}</div>
          <div class="el__index-front" data-index="{{ loop.index0 }}">Open</div>
        </div>
      </div>
      {% endfor %}

    </div>
  </div>

  {% else %}
    <div class="empty-state">
        <h2 class="empty-title"> Upload an image to get started</h2>
        <p class="empty-subtitle">
            Your analyzed images will appear here with color palettes, metrics, and visual cards.
        </p>

        <a href="/upload" class="empty-btn">Upload Image</a>
    </div>
  {% endif %}

  <script>
    document.addEventListener("DOMContentLoaded", function () {
      const cont = document.querySelector(".cont");
      if (cont) setTimeout(() => cont.classList.remove("s--inactive"), 50);

      const els = document.querySelectorAll(".el");
      let active = null;

      function activate(i) {
        els.forEach((el, idx) => {
          el.classList.toggle("el--active", idx === i);
        });
        cont.classList.add("s--active");
        active = i;
      }

      function reset() {
        els.forEach(el => el.classList.remove("el--active"));
        cont.classList.remove("s--active");
        active = null;
      }

      els.forEach((el, i) => {
        const openBtn = el.querySelector(".el__index-front");
        const closeBtn = el.querySelector(".el__close-btn");

        openBtn.addEventListener("click", e => {
          e.stopPropagation();
          active === i ? reset() : activate(i);
        });

        closeBtn.addEventListener("click", e => {
          e.stopPropagation();
          reset();
        });
      });
    });
  </script>

</body>
</html>
""")

# RENDER GALLERY FUNCTION
def render_gallery(uploads: list) -> str:
    return GALLERY_TEMPLATE.render(uploads=uploads)

# INDIVIDUAL REPORT TEMPLATE (old one kept as extra)
REPORT_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Color Analysis Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 30px;
            background: #fafafa;
            color: #333;
        }
    </style>
</head>

<body>
    <h1>Color Analysis Report</h1>

    <h2>Main Color</h2>
    <div style="width:120px;height:120px;border-radius:10px;background:rgb({{ main_color[0] }},{{ main_color[1] }},{{ main_color[2] }});"></div>

    <h2>Palette</h2>
    {% for c in dominant_colors %}
    <div style="width:60px;height:60px;display:inline-block;margin-right:8px;border-radius:8px;background:rgb({{ c[0] }},{{ c[1] }},{{ c[2] }});"></div>
    {% endfor %}

    <h2>Classification</h2>
    <p>Temperature: {{ temperature }}</p>
    <p>Brightness: {{ brightness }}</p>

    <h2>Metrics</h2>
    <ul>
        <li>Hue: {{ hue }}</li>
        <li>Saturation: {{ saturation }}</li>
        <li>Value: {{ value }}</li>
        <li>Luminance: {{ luminance }}</li>
    </ul>

</body>
</html>
""")

# GENERATE INDIVIDUAL REPORT FUNCTION
def generate_report_html(metrics: dict, filename: str, out_dir: str) -> str:
    ensure_dir(out_dir)

    html = REPORT_TEMPLATE.render(
        main_color=metrics["main_color"],
        dominant_colors=metrics["dominant_colors"],
        temperature=metrics["temperature"],
        brightness=metrics["brightness"],
        hue=metrics["hue"],
        saturation=metrics["saturation"],
        value=metrics["value"],
        luminance=metrics["luminance"],
    )

    safe_filename = filename.replace(" ", "_")
    report_path = os.path.join(out_dir, f"report_{safe_filename}.html")

    with open(report_path, "w") as f:
        f.write(html)

    return report_path
