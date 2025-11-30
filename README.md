# Case-Study Write-Up

## 1. Executive Summary
**Problem**: Artists, designers, and content creators often need a quick, automated way to extract a color palette and basic mood characteristics (light/dark, warm/cool) from reference images. Manually doing this in tools like Photoshop is slow and inconsistent.
**Solution**: A simple data pipeline + Flask API that accepts an image, extracts a palette using K-Means, determines the main color, computes HSV/luminance features, classifies the image temperature (warm/cool) and brightness (light/dark), and outputs both a JSON response and an auto-generated HTML dashboard.

## 2. System Overview 
**Course Concepts(s)**: Data Pipeline, Flask API, Deterministic Docker Container, Simple automated dashboard generation.
**Architecture Diagram**: assets/diagram.png
**Data/Models/Services**: 
- Input: user-uploaded images (JPG/PNG)
- Pipeline: Pillow, NumPy, sklearn KMeans
- Output: HTML dashboard + JSON metrics
- No external services or ML models required
- Licenses: All libraries are open-source and MIT/BSD licensed

## 3. How to Run (Local) 
```bash
./run.sh

# or, if no script provided:
docker build -t color-mood-analyzer .
docker run --rm -p 8080:8080 -v $(pwd)/assets:/app/assets color-mood-analyzer

```

## 4. Design Decisions
**Why this concept?**: A color-analysis pipeline is deterministic, lightweight, visually appealing, and easy to evaluate. It demonstrates a complete data workflow without requiring heavy ML.
**Tradeoffs**: 
- Using KMeans is simple and fast but not perceptually perfect.
- HSV temperature mapping is heuristic but interpretable.
- Flask is lighter than FastAPI but lacks built-in validation.
**Security/Privacy**: 
- No secrets required.
- No user data stored beyond optional saved images.
- All processing is local—no external API calls.
**Ops**: 
- Logs are simple Python prints (can be expanded).
- Stateless design—easy to scale using Docker.
- HTML report generation is fast and reproducible.

## 5. Results & Evaluation

Outputs include:
- Dominant color palette (5 RGB clusters)
- Main color
- Temperature classification (warm/cool)
- Brightness classification (light/dark)
- Luminance, hue, saturation, value
- HTML dashboard saved to: assets/reports/report_YYYYMMDD_HHMMSS.html

Example: 
```json
{
  "main_color": [173, 91, 50],
  "temperature": "warm",
  "brightness": "dark",
  "dominant_colors": [...],
  "dashboard_path": "assets/reports/report_20251127_154200.html"
}
Testing:
tests/test_health.py

```
## 6. What's Next?
- Add a Vue/React frontend
- Jinja2 templated dashboards
- Additional color science features (contrast ratios, harmony detection)

## 7. Links (Required)
**GitHub Repo**: <INSERT-REPO-URL>
**Public Cloud App (optional)**: <INSERT-CLOUD-URL>