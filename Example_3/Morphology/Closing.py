import cv2
import numpy as np
# The formula is: Closing = First Dilation + Then Erosion
# Without changing the overall size of the object, you fill in the spaces within and integrate the shape

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(300,300))

kernel = np.ones((5, 5), np.uint8)

# Closing Process
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

collage = cv2.hconcat([image,closing])
cv2.imshow("Original image --> Closing",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()