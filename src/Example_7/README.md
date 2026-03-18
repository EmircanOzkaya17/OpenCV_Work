# 🥝 Kiwi Segmentation Pipeline

An image processing pipeline that detects kiwi slices in a photo, applies individual **GrabCut** refinement for each kiwi, and produces a clean binary mask.

---

## 📋 Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration (.env)](#configuration-env)
- [Output Files](#output-files)
- [Project Structure](#project-structure)
- [Requirements](#requirements)

---

## Overview

This project combines classical computer vision techniques to detect and segment kiwi slices placed on a marble background. No deep learning models are used — only color space analysis, morphological operations, geometric filtering, and the GrabCut algorithm.

**Input:** A photo containing kiwi slices  
**Output:** A binary mask (kiwis = white, background = black) + overlay comparison images

---

## How It Works

The pipeline consists of 5 main stages:

### 1 — HSV Conversion & Saturation Thresholding
The image is converted from BGR to the HSV color space. Only the **S (Saturation)** channel is used; the marble background has very low saturation (S ≈ 5–13) while kiwi skin has high saturation (S ≈ 100–255). A threshold is applied to produce a raw binary mask.

### 2 — Morphological Noise Removal
Small pixel noise remaining in the binary mask is cleaned up with **Morphological OPEN** (Erosion + Dilation, 3×3 kernel). A small kernel is used deliberately to prevent kiwi blobs from merging together.

### 3 — Contour Analysis & Leaf Filtering
Raw contours found by `findContours` pass through a 4-stage filter:
- **Convex Hull** → Closes the hollow ring structure at the kiwi center, boosting circularity
- **Minimum area check** → Small residual blobs are discarded
- **Circularity filter** → Long, thin shapes (leaves) are eliminated
- **Aspect ratio filter** → Contours with a high ellipse axis ratio are eliminated

### 4 — GrabCut Refinement
Runs independently for each kiwi. The ellipse interior, center, and border are marked as distinct GrabCut regions (FGD / PR_FGD / PR_BGD / BGD). The algorithm decides kiwi vs. background pixel-by-pixel based on color statistics.

### 5 — Final Mask Generation
All individual kiwi masks are combined with a bitwise OR. The binary mask, overlay, and side-by-side comparison images are saved to disk.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/username/kiwi-segmentation.git
cd kiwi-segmentation

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

The application reads the `.env` file automatically. If the file is not found, it falls back to default values and prints a warning.

---

## Configuration (.env)

Create a `.env` file in the project root directory. Use `example.env` as a starting template.

| Variable | Default | Description |
|---|---|---|
| `IMAGE_PATH` | `assets/kiwi.jpg` | Full or relative path to the input image |
| `OUTPUT_DIR` | `results` | Directory where output images will be saved |
| `SATURATION_THRESHOLD` | `55` | HSV S-channel threshold (recommended: 45–70) |
| `MIN_AREA_RATIO` | `0.009` | Minimum blob area as a fraction of total pixels |
| `MAX_ASPECT_RATIO` | `2.0` | Maximum ellipse axis ratio (leaf filter) |
| `MIN_HULL_CIRCULARITY` | `0.40` | Convex hull circularity threshold |
| `ELLIPSE_SCALE` | `1.06` | Ellipse enlargement factor (compensates for edge loss) |
| `GRABCUT_ITERATIONS` | `4` | Number of GrabCut iterations (more = precise but slower) |
| `GRABCUT_BORDER_PX` | `18` | GrabCut border buffer width in pixels |
| `SAVE_INTERMEDIATE` | `True` | `True` → intermediate step images are also saved |

### Setup from template

```bash
cp example.env .env
# Then edit .env with your own paths and parameters
```

> ⚠️ Never push your `.env` file to Git. Make sure it is listed in `.gitignore`.

---

## Output Files

All outputs are written to the directory specified by `OUTPUT_DIR`.

| File | Description |
|---|---|
| `01_saturation_mask.jpg` | Raw saturation thresholding result |
| `02_cleaned_mask.jpg` | Mask after morphological noise removal |
| `03_debug_ellipses.jpg` | Detected ellipses drawn over the original image |
| `04_final_binary_mask.jpg` | Final binary mask (kiwi = white, background = black) |
| `05_overlay.jpg` | Semi-transparent green overlay on the original image |
| `06_comparison.jpg` | Original / Mask / Overlay side-by-side comparison |

> When `SAVE_INTERMEDIATE=False`, only files `04`, `05`, and `06` are produced.

---

## Project Structure

```
Example_7/
├── assets/
│   └── kiwi.jpg              # Input image
├── results/                  # Generated outputs (created automatically)
│   ├── 01_saturation_mask.jpg
│   ├── 02_cleaned_mask.jpg
│   ├── 03_debug_ellipses.jpg
│   ├── 04_final_binary_mask.jpg
│   ├── 05_overlay.jpg
│   └── 06_comparison.jpg
├── src/
│   └── app_func.py           # Core pipeline module
├── .env                      # Your local config (do NOT commit)
├── example.env               # Config template (safe to commit)
├── main.py                   # Entry point
├── README.md
└── requirements.txt
```

---

## Requirements

```
opencv-python
numpy
python-dotenv
```

To generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Technical Notes

- The pipeline is built entirely on classical image processing — no GPU or deep learning model required.
- GrabCut runs **independently** for each kiwi, preventing nearby kiwis from corrupting each other's mask.
- For different backgrounds or lighting conditions, `SATURATION_THRESHOLD` and `MIN_HULL_CIRCULARITY` are the primary parameters to tune first.