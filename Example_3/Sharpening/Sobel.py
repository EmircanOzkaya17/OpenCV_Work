import cv2
# Sobel looks at the 1st derivative
# Sobel is more robust to noise than Laplacian
# Sobel also has a Gaussian smoothing embedded in it when taking derivatives. Therefore, it is more robust to noise than Laplacian.
# The biggest difference of Sobel is that it is Directional.
# Horizontal Derivative (G_x) = [ [-1,0-1] , [-2,0,2] , [-1,0,1] ]
# Vertical Derivative (G_y) = [ [-1,-2,-1] , [0,0,0] , [1,2,1] ]

image =cv2.imread("petersburg.jpg")
image=cv2.resize(image,(400,400))


# dx=1, dy=0 -> Derivative only in the X direction (Vertical edges)
# dx=0, dy=1 -> Derivative only in the Y direction (Horizontal edges)
# ksize=3 -> 3x3 kernel

sobel_x = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
sobel_y = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)

# Converting to Absolute Value
# We convert negative slopes (white to black) to positive.

abs_sobel_x = cv2.convertScaleAbs(sobel_x)
abs_sobel_y = cv2.convertScaleAbs(sobel_y)

# Combining Two Directions (Gradient Magnitude)
# Approximate method: Add the two weighted (faster)
combined_sobel = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

collage= cv2.hconcat([image,abs_sobel_x,abs_sobel_y,combined_sobel])
cv2.imshow("Sobel", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()