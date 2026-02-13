import cv2 
import numpy as np 

img= cv2.imread(r"C:\OpenCV_Work\src\Example_5\assets\fruits.jpg")
img=cv2.resize(img,(640,640))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sharping. To better identify the contours
gray = cv2.Canny(img, threshold1=100, threshold2=200)

# Apply thresholding
# This step is important for separating objects from the background.
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


# Find contours 
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cv2.RETR_TREE --> This parameter determines which contours will be found and the relationship between them.
# Captures all contours.   Keeps nested relationships as a complete hierarchy

# Alternatives
#  cv2.RETR_EXTERNAL --> It only captures the outermost contours. If you're not interested in the inner details → THE FASTEST WAY
# cv2.RETR_LIST      --> All contours are captured. No hierarchy. Just a list.
# cv2.RETR_CCOMP     --> It divides the contours into 2 levels. Outer contours. Holes.

# cv2.CHAIN_APPROX_SIMPLE
# This parameter determines how the contour is stored. It discards unnecessary points.
# It removes intermediate points in the straight line.
# It only keeps the corner points.

# Alternatives
# cv2.CHAIN_APPROX_NONE
# It stores all pixels. It is preferred for sensitive analyses. It is slow and stores a lot of data.


# Draw the outlines onto the original image.
contour_image = img.copy()
cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)

cv2.imshow('Konturlu Görüntü', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Toplam {len(contours)} kontur bulundu.")