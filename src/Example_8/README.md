# Example_8 — Image Matching with ORB (Feature Matching)

An example project that extracts features (keypoints) using OpenCV's **ORB** (Oriented FAST and Rotated BRIEF) algorithm on **two images of the same scene/area taken from different angles**, and matches these features using the **BFMatcher** (Brute-Force Matcher).

The workflow consists of three steps:

1. Keypoints and descriptors are extracted from each image with ORB.
2. The descriptors of the two images are matched with BFMatcher.
3. The detected keypoints and matches are drawn and saved to the `results/` folder.

All settings are managed through a `.env` file, independent of the code, so you don't need to touch the source code to change parameters.

---

## 📁 Folder Structure

```
Example_8/
├── assets/
│   ├── image_1.jpeg          # 1st image (input)
│   └── image_2.jpeg          # 2nd image (input)
├── results/                  # Outputs are saved here (created automatically)
│   ├── keypoints_view1.jpg
│   ├── keypoints_view2.jpg
│   └── orb_matches.jpg
├── src/
│   ├── __init__.py           # Defines the 'src' package, exports ORBMatcher
│   └── orb_matcher.py        # Class containing the ORB + BFMatcher logic
├── .env                      # Actual config file (copied from example.env)
├── example.env               # Example/template config file
└── main.py                   # Program entry point
```

---

## ⚙️ Requirements

- Python 3.8+
- [opencv-python](https://pypi.org/project/opencv-python/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Installation:

```bash
pip install opencv-python python-dotenv
```

---

## 🔧 Setup and Configuration

Project settings are read from a `.env` file. A ready-made `example.env` template is included in the repo; copy it to create your own `.env` file:

```bash
# Inside the Example_8 folder
cp example.env .env
```

Parameters in the `.env` file:

### Image Paths

| Variable | Description | Default |
|----------|-------------|---------|
| `IMAGE_1_PATH` | Path of the 1st image (relative) | `assets/image_1.jpeg` |
| `IMAGE_2_PATH` | Path of the 2nd image (relative) | `assets/image_2.jpeg` |

### Output Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `RESULTS_DIR` | Folder where outputs are saved | `results` |
| `MATCHES_OUTPUT_NAME` | Name of the matches image | `orb_matches.jpg` |
| `KEYPOINTS_1_OUTPUT_NAME` | Name of the 1st image keypoints output | `keypoints_view1.jpg` |
| `KEYPOINTS_2_OUTPUT_NAME` | Name of the 2nd image keypoints output | `keypoints_view2.jpg` |

### ORB Parameters

| Variable | Description | Default |
|----------|-------------|---------|
| `ORB_N_FEATURES` | Maximum number of keypoints to retain | `1000` |
| `ORB_SCALE_FACTOR` | Pyramid scale factor | `1.2` |
| `ORB_N_LEVELS` | Number of pyramid levels | `8` |
| `ORB_EDGE_THRESHOLD` | Edge threshold (filters out keypoints near edges) | `31` |
| `ORB_PATCH_SIZE` | Patch size used for the descriptor | `31` |
| `ORB_FAST_THRESHOLD` | FAST corner detector threshold | `20` |

### BFMatcher Parameters

| Variable | Description | Default |
|----------|-------------|---------|
| `BF_NORM_TYPE` | Distance metric (`NORM_HAMMING`, `NORM_HAMMING2`, `NORM_L1`, `NORM_L2`) | `NORM_HAMMING` |
| `BF_CROSS_CHECK` | Cross-check (mutual best matches) | `True` |
| `MATCHES_TO_DRAW` | Number of best matches to draw | `50` |

> **Note:** Since ORB produces binary descriptors, it is recommended to use `NORM_HAMMING` as `BF_NORM_TYPE`.

---

## ▶️ Running

From inside the `Example_8` folder:

```bash
python main.py
```

Regardless of which directory it is run from, the program bases everything on the folder where `main.py` is located; therefore relative paths (`assets/...`, `results/...`) are resolved without issues.

Example terminal output:

```
[ORB] 1. gorsel: 1000 keypoint
[ORB] 2. gorsel: 1000 keypoint
[KAYIT] .../results/keypoints_view1.jpg
[KAYIT] .../results/keypoints_view2.jpg
[BFMatcher] Toplam 312 eslesme bulundu
[KAYIT] En iyi 50 eslesme -> .../results/orb_matches.jpg

Islem tamamlandi. Sonuclar 'results/' klasorunde.
```

---

## 📤 Outputs

After running, three images are created in the `results/` folder:

- **`keypoints_view1.jpg`** — The ORB keypoints detected on the 1st image (rich keypoint drawing: with location, size and orientation).
- **`keypoints_view2.jpg`** — The ORB keypoints detected on the 2nd image.
- **`orb_matches.jpg`** — The two images side by side, with lines showing the best matches between them.

---

## 🧩 Code Structure

### `main.py`
The entry point of the program. It does the following in order:
1. Reads the `.env` file (`load_config`).
2. Creates an `ORBMatcher` instance.
3. Loads the images both in grayscale (for ORB) and in color (for drawing).
4. Extracts keypoints and descriptors, saves the keypoint images.
5. Matches the descriptors.
6. Draws and saves the best matches.

### `src/orb_matcher.py`
Contains the `ORBMatcher` class that encapsulates all image processing logic:

- `load_image()` — Reads the image in grayscale/color; raises a meaningful error if the file is missing or corrupt.
- `detect_and_compute()` — Extracts keypoints and descriptors with ORB.
- `match_descriptors()` — Matches with BFMatcher and sorts the results by distance (best to worst).
- `draw_keypoints()` — Draws keypoints on a single image.
- `draw_matches()` — Draws matches between two images.
- `save_result()` — Saves the result under `RESULTS_DIR`.

### `src/__init__.py`
Makes the `src` folder a Python package and allows `ORBMatcher` to be accessed both as
`from src import ORBMatcher` and `from src.orb_matcher import ORBMatcher`.

---

## 📝 Notes

- The `.env` file may contain personal/local settings; if you don't want it pushed to the repo, it's recommended to add it to `.gitignore`. Use `example.env` as the shared template.
- Match quality depends on the amount of overlap between the images and their texture richness. If you get few matches, try increasing `ORB_N_FEATURES` or lowering `ORB_FAST_THRESHOLD`.
