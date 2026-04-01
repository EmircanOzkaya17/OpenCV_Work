# 🥝 Kiwi Detector — OpenCV HSV Filtering

A computer vision pipeline that detects and segments kiwi fruits from images using HSV color masking, morphological operations, and contour filtering.

---

## 📁 Project Structure

```
Example_7/
├── assets/
│   └── kiwi.jpg                  # Input image
├── results/                      # Auto-generated step-by-step outputs
│   ├── 01_original_bgr.jpg
│   ├── 02_hsv_conversion.jpg
│   ├── 03_raw_mask.jpg
│   ├── 04_masked_hsv.jpg
│   ├── 05_morphology_01_opening.jpg
│   ├── 06_morphology_02_closing.jpg
│   ├── 07_morphology_03_erosion.jpg
│   └── 08_result_drawing.jpg
├── src/
│   └── app_func.py               # KiwiFilter class (core logic)
├── .env                          # Environment variables (not committed)
├── example.env                   # Example environment file
├── main.py                       # Entry point
└── README.md
```

---

## ⚙️ How It Works

The pipeline consists of 5 sequential steps:

1. **Load Image** — Reads the input image in BGR format.
2. **HSV Conversion** — Converts BGR to HSV color space for more robust color filtering.
3. **Green/Yellow Mask** — Creates a binary mask targeting the green-yellow HSV range of kiwi skin.
4. **Morphological Operations** — Applies opening, closing, and erosion to clean up noise and refine the mask.
5. **Contour Detection** — Filters contours by area, circularity, and convexity; draws valid detections on a black canvas.

Each step automatically saves its output image to the `results/` directory.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install dependencies

```bash
pip install opencv-python numpy python-dotenv
```

### 3. Configure environment variables

Copy `example.env` to `.env` and update the paths:

```bash
cp example.env .env
```

Then edit `.env`:

```env
INPUT_IMAGE_PATH="path/to/your/image.jpg"
OUTPUT_IMAGE_PATH="path/to/your/results"
```

### 4. Run

```bash
python main.py
```

---

## 🔧 Configuration

All parameters are controlled via the `.env` file.

| Variable                        | Default      | Description                                  |
|---------------------------------|--------------|----------------------------------------------|
| `INPUT_IMAGE_PATH`              | `kiwi.jpg`   | Path to the input image                      |
| `OUTPUT_IMAGE_PATH`             | `output.jpg` | Path to the results directory                |
| `HSV_H_MIN`                     | `25`         | Hue lower bound (yellowish start)            |
| `HSV_H_MAX`                     | `85`         | Hue upper bound (end of green)               |
| `HSV_S_MIN`                     | `40`         | Saturation lower bound (filters background)  |
| `HSV_S_MAX`                     | `255`        | Saturation upper bound                       |
| `HSV_V_MIN`                     | `110`        | Value lower bound (filters out dark leaves)  |
| `HSV_V_MAX`                     | `255`        | Value upper bound                            |
| `MORPH_KERNEL_SIZE`             | `5`          | Morphological kernel size                    |
| `MORPH_OPEN_ITERATIONS`         | `2`          | Opening iterations (removes small noise)     |
| `MORPH_CLOSE_ITERATIONS`        | `3`          | Closing iterations (fills gaps)              |
| `MORPH_ERODE_ITERATIONS`        | `1`          | Erosion iterations after closing             |
| `CONTOUR_MIN_AREA`              | `1000`       | Minimum contour area (px²)                   |
| `CONTOUR_MAX_AREA`              | `500000`     | Maximum contour area (px²)                   |
| `CONTOUR_CIRCULARITY_THRESHOLD` | `0.45`       | Minimum circularity score                    |
| `CONTOUR_CONVEXITY_THRESHOLD`   | `0.65`       | Minimum convexity score (for wedge shapes)   |

---

