import cv2 
import numpy as np
# Kernel (Structuring Element) is used
# If all pixels below the kernel are "1" (white), the center pixel is preserved (remains white). 
# However, if there is even a single "0" (black) below the kernel, the center pixel is made a "0" (converted to black/deleted).

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(300,300))

# Creating the Kernel (Structuring Element)
# We create a 5x5 matrix filled with 1s.

kernel = np.ones((5, 5), np.uint8)

# Applying the Erosion Process

erosion = cv2.erode(image, kernel, iterations=1) # iterations=1 means the operation is performed once

collage=cv2.hconcat([image,erosion])
cv2.imshow("Original image --> Erosion",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
