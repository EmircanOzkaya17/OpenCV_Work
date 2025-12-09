import cv2
import numpy as np
# The Laplacian operator is based on the second derivative logic in the image.
# A standard 3x3 Laplacian kernel that performs this calculation is as follows:
# [ [0,1,0] , [1,-4,1] , [0,1,0] ]

# Working Principle:
# Multiplies the center pixel by a negative coefficient (e.g., -4).
# Multiplies neighboring pixels by a positive coefficient (+1).
# If the center pixel and its neighbors are the same color (solid area), the result is 0.
# If there is a difference (edge), the result is a large value other than 0.

image =cv2.imread("petersburg.jpg")
image=cv2.resize(image,(500,500))
image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Laplacian Implementation
# ddepth=cv2.CV_64F: We use 64-bit float to avoid losing negative values.
# ksize=3: Use a 3x3 kernel (mask).
laplacian = cv2.Laplacian(src=image_gray, ddepth=cv2.CV_64F, ksize=3)

 
# Converting to Absolute Value
# We convert negative derivative values ​​to positive and convert them to uint8 (0-255) format.
laplacian_abs = cv2.convertScaleAbs(laplacian)

# Sharpening Process
# Logic: Original Image - (Coefficient * Laplacian Edges)
# Since the center of our Laplacian kernel is negative, we are subtracting here.
# So, negative and negative come together to create an additive effect, strengthening the central pixel.
sharpened_image = cv2.addWeighted(image_gray, 1.5, laplacian_abs, -0.5, 0)

laplacian_norm = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX)
laplacian_norm = np.uint8(laplacian_norm)

collage=cv2.hconcat([image_gray,laplacian_norm,laplacian_abs,sharpened_image])
cv2.imshow("Collage",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
