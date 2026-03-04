import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread(r"C:\OpenCV_Work\assets\petersburg.jpg", cv2.IMREAD_GRAYSCALE)
img=cv2.resize(img, (640,640))

# Apply histogram equalization
equalized_img = cv2.equalizeHist(img)

# Show results
cv2.imshow('Original Image', img)
cv2.imshow('Histogram Synchronized', equalized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Comparison of histograms
plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.hist(img.ravel(), 256, [0,256])
plt.title('Original Histogram')

plt.subplot(1,2,2)
plt.hist(equalized_img.ravel(), 256, [0,256])
plt.title('Synchronized Histogram')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()