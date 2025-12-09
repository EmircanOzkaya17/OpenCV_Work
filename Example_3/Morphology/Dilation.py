import cv2
import numpy as np
# How it works: The kernel slides over the image pixel by pixel.
# Rule: If there's even a single "1" (white) pixel in the area covered by the kernel, it sets the center pixel to "1" (white).

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(300,300))
kernel = np.ones((5, 5), np.uint8)

# Applying the Dilation Process
# iterations = 1 -> The process is applied once.
# If you increase the number, the object will gradually expand.

dilation = cv2.dilate(image, kernel, iterations=1)

collage = cv2.hconcat([image,dilation])
cv2.imshow("Original image --> Dilation",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()