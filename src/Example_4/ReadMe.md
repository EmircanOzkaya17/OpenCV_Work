# Example 4: Image Thresholding & Color Manipulation

This project focuses on fundamental **Thresholding techniques**, which are essential for image segmentation, and their practical application in **Color Manipulation**, using the OpenCV library.

---

## 📂 Project Structure

Below is the complete directory tree for this project:

```text
Example_4/
├── assets/
│   └── rose.jpg               # Original input image
├── results/                   # Processed output images
│   ├── adaptive_gaussian.png
│   ├── adaptive_mean.png
│   ├── binary_image.png
│   ├── otsu_imahe.png
│   ├── rose_mask.png
│   └── rose_purple.png
├── src/
│   ├── application.py         # Script for color manipulation (Red to Purple)
│   └── tresholding.py         # Class containing thresholding algorithms
├── main.py                    # Main entry point to run and test the project
└── ReadMe.md                  # Project documentation

---

## 🛠 Techniques Used

### 1. Image Thresholding
The following methods were utilized to separate pixels in the image based on specific criteria:

* **Binary Thresholding**: Pixels above a fixed threshold value (e.g., 60) are set to white (255), while those below are set to black (0).
* **Otsu’s Thresholding**: Automatically determines the optimal threshold value by analyzing the image histogram.
* **Adaptive Thresholding**: Computes local thresholds for different regions of the image to handle illumination variations.
    * **Mean**: Uses the average value of the neighboring region.
    * **Gaussian**: Uses a weighted sum of the neighborhood, giving more importance to pixels closer to the center.

### 2. Color Manipulation (Application)
The following steps were applied to change the color of the rose from red to purple:

1.  **HSV Conversion**: The image was converted from the BGR color space to the HSV color space.
2.  **Color Masking**: Two separate masks for red tones (`lower_red` and `upper_red`) were created and then combined.
3.  **Morphological Operations**: **MORPH_CLOSE** (closing) and **MORPH_OPEN** (opening) operations were applied to remove noise from the mask.
4.  **Color Change**: The Hue value of the masked region was set to 135 (purple), and the Saturation was increased by 50%.