<p align="center"> <img src="../../assets/logo.png" alt="OpenCv Works" width="250"> </p>
Example 5 – Fruit Counting & Contour Analysis
This example demonstrates a complete interactive fruit counting application and a contour feature extraction tool using OpenCV.
It is designed to teach core computer vision concepts such as edge detection, contour finding, geometric property calculation, and real‑time parameter tuning via trackbars.

📚 Table of Contents
🎯 What This Example Demonstrates

📁 Project Structure

🚀 How to Run

🎯 What This Example Demonstrates
Image Loading & Preprocessing: Reading an image, converting to grayscale, applying Gaussian blur.

Canny Edge Detection: Interactive adjustment of lower and upper thresholds using trackbars.

Contour Detection & Filtering: Finding external contours and filtering them by minimum/maximum area.

Object Counting & Labeling: Drawing green bounding contours around detected fruits and numbering them at their centroids.

Real‑Time Parameter Control: Trackbars allow live modification of Canny thresholds and area limits.

Result Export: Saving the processed image and the edge map with a single key press.

New Image Selection: Loading a different image via a file dialog (Tkinter).

Detailed Contour Analysis: The features.py script computes and visualises for each contour:

Area, perimeter, centroid

Bounding rectangle, minimum area rectangle, minimum enclosing circle
Aspect ratio, extent (fill ratio), solidity (convexity)

All results are saved as individual images in a results/ folder.


📁 Project Structure
The files inside src/Example_5/ are organised as follows:
src/Example_5/
├── assets/                          # Sample image used by default
│   └── fruits.jpg
├── results/                        # Created automatically by features.py
│   ├── original.jpg
│   ├── gray.jpg
│   ├── edges.jpg
│   ├── thresh.jpg
│   ├── all_contours.jpg
│   └── contour_0.jpg, contour_1.jpg, ...
├── main.py                          # Interactive fruit counting application
└── src/                            
├── application_func.py        # ImageProcessor class – core logic
├── draw_contours.py           # Simple contour drawing test script
└── features.py               # Advanced contour feature extraction & visualisation


application_func.py
Defines the ImageProcessor class. Handles image loading, Canny edge detection, contour retrieval, area filtering, object numbering, and info overlay. Also provides methods to update parameters, reset to defaults, and save results.

main.py
The entry point for the interactive fruit counter. Creates two windows (“Fruit Counting” and “Edge Detection”), adds four trackbars (Canny Th1, Canny Th2, Min Area, Max Area), and processes keyboard commands:

q – quit

r – reset parameters

s – save processed image and edge map

n – open file dialog to load a new image

draw_contours.py
A minimal script that loads fruits.jpg, applies Canny and thresholding, finds all contours, and draws them in red. Useful for quick contour visualisation.

features.py
An extended analysis tool. It loads the image, applies Canny and binary thresholding, finds all contours (using RETR_TREE), and for each contour calculates a wide set of geometric properties. Every contour is saved as a separate image with its bounding shapes overlaid. All intermediate stages and a composite image of all contours are also stored in the results/ folder.

🚀 How to Run
1. Interactive Fruit Counting
Make sure you are in the project root directory and your virtual environment is activated. Then run:

bash
python "src/Example_5/main.py"
The default image assets/fruits.jpg will be loaded.

Adjust the trackbars to see the effect on edge detection and fruit counting in real time.

Use the keyboard commands listed above.

2. Contour Feature Extraction
To generate detailed contour analyses and save all output images:

bash
python "src/Example_5/features.py"
All images will be saved inside the automatically created src/Example_5/results/ folder.

Press any key while a contour window is active to advance to the next contour.