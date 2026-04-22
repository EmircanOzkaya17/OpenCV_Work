<p align="center">
  <img src="assets/logo.png" alt="OpenCV Works" width="220"/>
</p>

<h1 align="center">🔬 OpenCV Work — Practical Computer Vision with Python</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/NumPy-1.x-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Matplotlib-visualization-orange?style=for-the-badge" alt="Matplotlib">
</p>

<p align="center">
  A structured collection of hands-on OpenCV examples covering the fundamentals of computer vision — from basic image operations to real-time object detection. Each example is self-contained with its own assets, source code, and results folder.
</p>

---

## 📚 Table of Contents

1. [🗂 Repository Structure](#-repository-structure)
2. [⚡ Quick Start](#-quick-start)
3. [🧩 Examples Overview](#-examples-overview)
   - [Example 1 — Basic Image Operations](#example-1--basic-image-operations)
   - [Example 2 — Geometric Transformations](#example-2--geometric-transformations)
   - [Example 3 — Image Filtering & Blurring](#example-3--image-filtering--blurring)
   - [Example 4 — Thresholding & Color Manipulation](#example-4--thresholding--color-manipulation)
   - [Example 5 — Fruit Counting & Contour Analysis](#example-5--fruit-counting--contour-analysis)
   - [Example 6 — Histogram Processing](#example-6--histogram-processing)
   - [Example 7 — Kiwi Detector (HSV Filtering)](#example-7--kiwi-detector-hsv-filtering)
4. [🛠 Technologies Used](#-technologies-used)
5. [🔧 Installation](#-installation)
6. [📁 Full Directory Tree](#-full-directory-tree)

---

## 🗂 Repository Structure

Each example lives under `src/Example_N/` and follows a consistent layout:

```text
src/Example_N/
├── assets/         # Input images
├── results/        # Auto-generated output images
├── src/            # Core logic / helper classes
├── main.py         # Entry point
└── ReadMe.md       # Example-specific documentation
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/EmircanOzkaya17/OpenCV_Work.git
cd OpenCV_Work
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install opencv-python numpy matplotlib python-dotenv
```

### 4. Run any example

```bash
python src/Example_4/main.py
```

---

## 🧩 Examples Overview

---

### Example 1 — Basic Image Operations

> Reading, displaying, writing, resizing, and cropping images using OpenCV.

**Key concepts:** `cv2.imread`, `cv2.imshow`, `cv2.imwrite`, slicing, resizing, color space conversions (BGR → RGB, BGR → Grayscale).

```bash
python src/Example_1/main.py
```

---

### Example 2 — Geometric Transformations

> Applying spatial transformations to images: translation, rotation, scaling, flipping, and perspective warping.

**Key concepts:** `cv2.warpAffine`, `cv2.getRotationMatrix2D`, `cv2.flip`, `cv2.getPerspectiveTransform`.

```bash
python src/Example_2/main.py
```

---

### Example 3 — Image Filtering & Blurring

> Reducing noise and enhancing image quality using various filtering techniques.

**Key concepts:** Gaussian blur, median blur, bilateral filter, 2D convolution with custom kernels (`cv2.filter2D`), sharpening.

```bash
python src/Example_3/main.py
```

---

### Example 4 — Thresholding & Color Manipulation

> Segmenting images with thresholding algorithms and applying HSV-based color changes.

**Techniques covered:**

| Technique | Description |
|---|---|
| Binary Thresholding | Pixels above a fixed value → white; below → black |
| Otsu's Thresholding | Automatically finds the optimal threshold from the histogram |
| Adaptive Mean | Local threshold using the mean of the neighborhood |
| Adaptive Gaussian | Local threshold using a Gaussian-weighted neighborhood |
| Color Change (HSV) | Red rose → purple via hue shift + saturation boost |

**Morphological operations used:** `MORPH_CLOSE` (closing) and `MORPH_OPEN` (opening) to clean up the color mask.

```bash
python src/Example_4/main.py
```

**Project structure:**
```text
Example_4/
├── assets/rose.jpg
├── results/
│   ├── adaptive_gaussian.png
│   ├── adaptive_mean.png
│   ├── binary_image.png
│   ├── otsu_image.png
│   ├── rose_mask.png
│   └── rose_purple.png
├── src/
│   ├── application.py      # Color manipulation (Red → Purple)
│   └── tresholding.py      # Thresholding class
└── main.py
```

---

### Example 5 — Fruit Counting & Contour Analysis

> An interactive fruit counting application with real-time parameter tuning via trackbars, plus a detailed contour feature extraction tool.

**What this example demonstrates:**

- Image preprocessing: grayscale conversion, Gaussian blur
- Canny edge detection with interactive threshold control
- Contour detection and area-based filtering
- Object counting and centroid labeling
- Saving results with a single key press
- Loading a new image via file dialog (Tkinter)
- Per-contour geometric property analysis: area, perimeter, bounding rectangle, min-area rectangle, enclosing circle, aspect ratio, extent, and solidity

**Keyboard controls (main.py):**

| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Reset parameters to defaults |
| `s` | Save processed image and edge map |
| `n` | Load a new image via file dialog |

```bash
# Interactive fruit counter
python src/Example_5/main.py

# Detailed contour feature extraction (saves all outputs to results/)
python src/Example_5/src/features.py
```

**Project structure:**
```text
Example_5/
├── assets/fruits.jpg
├── results/
│   ├── original.jpg
│   ├── gray.jpg
│   ├── edges.jpg
│   ├── thresh.jpg
│   ├── all_contours.jpg
│   └── contour_0.jpg, contour_1.jpg, ...
├── src/
│   ├── application_func.py    # ImageProcessor class (core logic)
│   ├── draw_contours.py       # Quick contour visualisation
│   └── features.py            # Advanced contour feature extraction
└── main.py
```

---

### Example 6 — Histogram Processing

> Computing, equalizing, and visualizing grayscale histograms for contrast enhancement.

**Features:**

- Load and process grayscale images
- Compute histograms as line and bar charts
- Apply histogram equalization for contrast enhancement
- Side-by-side comparison of original and equalized images
- Save all results at high resolution (300 dpi)
- Configurable via `.env` file

**Output files:**

| File | Description |
|---|---|
| `Gray Level Histogram.png` | Line plot of the grayscale histogram |
| `Gray Level Histogram (Bar).png` | Bar chart of the same histogram |
| `histogram_comparison.png` | Original vs. equalized image with both histograms |

```bash
# Histogram equalization with comparison
python src/Example_6/src/main.py

# Manual histogram plotting only
python src/Example_6/src/drawing_histogram_gray.py
```

**Environment setup:**
```bash
cp src/Example_6/example.env src/Example_6/.env
# Edit .env to set IMG_PATH and RESULTS_PATH
```

**Project structure:**
```text
Example_6/
├── assets/petersburg.jpg
├── results/
│   ├── Gray Level Histogram.png
│   ├── Gray Level Histogram (Bar).png
│   └── histogram_comparison.png
├── src/
│   ├── app_func.py                  # HistogramProcessing class
│   ├── drawing_histogram_gray.py    # Manual histogram plotting
│   └── main.py                      # Main entry point
├── example.env
└── README.md
```

---

### Example 7 — Kiwi Detector (HSV Filtering)

> A complete 5-step computer vision pipeline that detects and segments kiwi fruits using HSV color masking, morphological cleaning, and contour filtering.

**Pipeline steps:**

```
1. Load Image       →  Read BGR image from disk
2. HSV Conversion   →  Convert BGR → HSV for robust color filtering
3. Green/Yellow Mask→  Binary mask targeting kiwi skin color range
4. Morphology       →  Opening + Closing + Erosion to refine the mask
5. Contour Detection→  Filter by area, circularity & convexity; draw on canvas
```

Each step automatically saves its output to `results/`.

**Configurable parameters (`.env`):**

| Variable | Default | Description |
|---|---|---|
| `HSV_H_MIN` / `HSV_H_MAX` | `25` / `85` | Hue range (yellow → green) |
| `HSV_S_MIN` / `HSV_S_MAX` | `40` / `255` | Saturation range |
| `HSV_V_MIN` / `HSV_V_MAX` | `110` / `255` | Value range (filters dark areas) |
| `MORPH_KERNEL_SIZE` | `5` | Morphological kernel size |
| `MORPH_OPEN_ITERATIONS` | `2` | Opening passes (removes noise) |
| `MORPH_CLOSE_ITERATIONS` | `3` | Closing passes (fills gaps) |
| `MORPH_ERODE_ITERATIONS` | `1` | Erosion passes after closing |
| `CONTOUR_MIN_AREA` | `1000` | Minimum contour area (px²) |
| `CONTOUR_MAX_AREA` | `500000` | Maximum contour area (px²) |
| `CONTOUR_CIRCULARITY_THRESHOLD` | `0.45` | Minimum circularity score |
| `CONTOUR_CONVEXITY_THRESHOLD` | `0.65` | Minimum convexity score |

```bash
cp src/Example_7/example.env src/Example_7/.env
# Edit .env to set INPUT_IMAGE_PATH and OUTPUT_IMAGE_PATH
python src/Example_7/main.py
```

**Project structure:**
```text
Example_7/
├── assets/kiwi.jpg
├── results/
│   ├── 01_original_bgr.jpg
│   ├── 02_hsv_conversion.jpg
│   ├── 03_raw_mask.jpg
│   ├── 04_masked_hsv.jpg
│   ├── 05_morphology_01_opening.jpg
│   ├── 06_morphology_02_closing.jpg
│   ├── 07_morphology_03_erosion.jpg
│   └── 08_result_drawing.jpg
├── src/app_func.py     # KiwiFilter class
├── example.env
└── main.py
```

---

## 🛠 Technologies Used

| Library | Version | Purpose |
|---|---|---|
| **Python** | 3.x | Core language |
| **OpenCV** (`cv2`) | 4.x | Image processing, detection, morphology |
| **NumPy** | 1.x | Array operations |
| **Matplotlib** | latest | Histogram plotting & visualization |
| **python-dotenv** | latest | Environment variable management |
| **Tkinter** | stdlib | File dialog (Example 5) |

---

## 🔧 Installation

```bash
pip install opencv-python numpy matplotlib python-dotenv
```

> **Note:** Some examples use a `.env` file for path and parameter configuration. Copy the provided `example.env` to `.env` and update the values before running.

---

## 📁 Full Directory Tree

```text
OpenCV_Work/
├── assets/
│   └── logo.png
├── src/
│   ├── Example_1/          # Basic image operations
│   ├── Example_2/          # Geometric transformations
│   ├── Example_3/          # Image filtering & blurring
│   ├── Example_4/          # Thresholding & color manipulation
│   ├── Example_5/          # Fruit counting & contour analysis
│   ├── Example_6/          # Histogram processing
│   └── Example_7/          # Kiwi detector (HSV filtering)
└── README.md
```

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/EmircanOzkaya17">EmircanOzkaya17</a>
</p>