import cv2
# Sobel and Laplacian give us "rough" results (thick lines, noise). 
# Canny, on the other hand, gives us thin, clean, and continuous lines. 
# It's considered the "Gold Standard of Edge Detection" in image processing.

# The Logic of the Canny Algorithm (4-Step Process)
# Canny is not a single operation, but a chain of algorithms. It follows these steps:

# Noise Reduction (Gaussian Blur): Canny is very sensitive to noise. 
# Therefore, before starting, it blurs the image slightly (using a 5x5 Gaussian Kernel) to prevent 
# the "noise" from being mistaken for edges.

# Gradient Calculation (Sobel Step):

# Non-Maximum Suppression - Thinning Step: The edges resulting from the Sobel algorithm are thick and blurry. 
# Canny scans along this thick line, keeping only the peak (the brightest pixel) and removing the rest.

# Result: Thick edges are converted to single-pixel thin lines.

# Hysteresis Thresholding - Reasoning Step: This is the most critical part. Two threshold values ​​(thresholds) are determined: 
# MinVal and MaxVal.


image = cv2.imread('petersburg.jpg', 0) #To get the image in 0 grayscale
image=cv2.resize(image,(700,500))

canny_edges = cv2.Canny(image, threshold1=100, threshold2=200)
collage=cv2.hconcat([image,canny_edges])

cv2.imshow(" ", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Critical Point: Threshold Values ​​(100 and 200)
#The threshold1 and threshold2 parameters you'll see in the code determine Canny's character:

# Narrowing the Range (e.g., 50 - 100): It treats too much detail and noise as edges. The image becomes more complex.

# Increasing the Range (e.g., 150 - 250): It draws only very distinct outlines and loses fine details.

# It's perfect for "object detection" and "shape analysis" rather than "sharpening".