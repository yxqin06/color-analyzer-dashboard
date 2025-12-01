import io
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# Load image
def load_image_bytes(b: bytes) -> Image.Image:
    # Load image bytes into a PIL Image.
    return Image.open(io.BytesIO(b)).convert("RGB")

# classify warm/cool
def classify_temperature(hue: float) -> str:
    # Hue: 0–360 degrees
    # Warm: reds, oranges, yellows → 0–60 or 300–360
    # Cool: blues, greens → 60–300
    if hue < 60 or hue > 300:
        return "warm"
    return "cool"


# classify light/dark
def classify_brightness(value: float) -> str:
    # Value (HSV) ranges 0–1
    return "light" if value > 0.5 else "dark"


# Compute dominant colors, main color, and features
def compute_color_features(img: Image.Image) -> dict:
    """
    Extract:
      - Dominant color palette (KMeans)
      - Main color (largest cluster)
      - HSV + luminance
      - Warm/cool + light/dark classification
    """
    img_small = img.resize((150, 150))  # speed up KMeans
    arr = np.array(img_small)
    pixels = arr.reshape(-1, 3)

    # KMeans to extract 5 colors
    kmeans = KMeans(n_clusters=5, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_.astype(int)

    # Sort palette by size of cluster
    counts = np.bincount(labels)
    sorted_idx = np.argsort(counts)[::-1]

    dominant_colors = [centers[i].tolist() for i in sorted_idx]
    main_color = dominant_colors[0]

    # Convert main color to HSV + luminance
    r, g, b = np.array(main_color) / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    # Hue
    if diff == 0:
        hue = 0
    elif mx == r:
        hue = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        hue = (60 * ((b - r) / diff) + 120) % 360
    else:
        hue = (60 * ((r - g) / diff) + 240) % 360

    # Saturation
    sat = 0 if mx == 0 else diff / mx

    # Value
    val = mx

    # Luminance
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # Classifications
    temperature = classify_temperature(hue)
    brightness = classify_brightness(val)

    return {
        "main_color": main_color,
        "dominant_colors": dominant_colors,
        "hue": hue,
        "saturation": sat,
        "value": val,
        "luminance": luminance,
        "temperature": temperature,
        "brightness": brightness,
    }
