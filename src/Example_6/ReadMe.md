This project demonstrates histogram calculation, histogram equalization (contrast enhancement), and visualization of results on grayscale images using the OpenCV library. It provides two approaches: manual histogram plotting and class-based histogram equalization with comparative visualization.

🚀 Features
Load grayscale images

Compute histograms (line and bar charts)

Apply histogram equalization (contrast enhancement)

Side-by-side comparison of original and equalized images

Visual comparison of histograms

Save results to a specified folder

Example_6/
├── assets/
│   └── petersburg.jpg          # Sample input image
├── results/                     # Output folder for generated images
│   ├── Gray Level Histogram.png
│   ├── Gray Level Histogram (Bar).png
│   └── histogram_comparison.png
├── src/
│   ├── app_func.py              # HistogramProcessing class (core functionality)
│   ├── drawing_histogram_gray.py # Manual histogram plotting (line + bar)
│   ├── histogram_equalization.py # (optional, may contain similar code)
│   └── main.py                   # Main application entry point
├── example.env                   # Example environment variables file
└── README.md                      # This file



🛠️ Technologies Used
Python 3.x

OpenCV (cv2) – Image processing and histogram calculations

NumPy – Array operations

Matplotlib – Plotting and visualization

python-dotenv – Managing environment variables

⚙️ Installation
Clone the repository (or download the project files):
git clone https://github.com/EmircanOzkaya17/OpenCV_Work.git
cd OpenCV_Work/src/Example_6

Install required libraries:

bash
pip install opencv-python numpy matplotlib python-dotenv

Set up environment variables:
Copy the example.env file to create your own .env file:

bash
cp example.env .env
Edit the .env file to set IMG_PATH and RESULTS_PATH according to your system

🧪 Usage
1. Histogram Equalization and Comparison (Main Application)
bash
python src/main.py
This command will:

Load the image specified in the .env file.

Apply histogram equalization.

Generate a side-by-side comparison of the original and equalized images along with their histograms.

Save the result as results/histogram_comparison.png.

2. Manual Histogram Plotting
bash
python src/drawing_histogram_gray.py
This script will:

Load the sample image (petersburg.jpg).

Create two histogram plots: a line plot and a bar plot.

Save the plots as PNG files in the results/ folder.

Display the plots on the screen.

📊 Output Examples
Gray Level Histogram.png: Line plot of the grayscale histogram.

Gray Level Histogram (Bar).png: Bar chart of the same histogram.

histogram_comparison.png: Comparison of original and equalized images with their histograms.

📝 Notes
All images are processed as grayscale.

Output images are saved at high resolution (300 dpi).

The HistogramProcessing class in app_func.py modularizes the histogram equalization tasks and can be reused in other projects.