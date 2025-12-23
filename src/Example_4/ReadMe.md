Example 4: Image Thresholding & Color Manipulation

This project focuses on fundamental Thresholding techniques, which are essential for image segmentation, and their practical application in Color Manipulation, using the OpenCV library.

📂 Folder Structure and Files

tresholding.py: Contains a class that implements different thresholding algorithms (Binary, Otsu, Adaptive).

main.py: The main file that tests the thresholding methods and visualizes the results.

application.py: An application that detects a red rose and changes its color to purple.

rose.jpg: The original input image used in the processing steps.

results: Images obtained according to the applied processes.


🛠 Techniques Used

1. Image Thresholding

The following methods were used to separate pixels in the image based on specific criteria:

Binary Thresholding: Pixels above a fixed threshold value (e.g., 60) are set to white (255), while those below are set to black (0).

Otsu’s Thresholding: Automatically determines the optimal threshold value by analyzing the image histogram.

Adaptive Thresholding: Computes local thresholds for different regions of the image to handle illumination variations.

Mean: Uses the average value of the neighboring region.

Gaussian: Uses a weighted sum of the neighborhood, giving more importance to pixels closer to the center.

2. Color Manipulation (Application)

The following steps were applied to change the color of the rose from red to purple:

HSV Conversion: The image was converted from the BGR color space to HSV.

Color Masking: Two separate masks for red tones (lower_red and upper_red) were created and then combined.

Morphological Operations: MORPH_CLOSE (closing) and MORPH_OPEN (opening) operations were applied to remove noise from the mask.

Color Change: The Hue value of the masked region was set to 135 (purple), and the Saturation was increased by 50%.


