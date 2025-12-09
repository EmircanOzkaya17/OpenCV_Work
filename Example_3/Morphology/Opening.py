import cv2
import numpy as np
# The formula is: Opening = First Erosion + Then Dilation
# By preserving the object's size, you clear out any noise that might appear as "fly droppings" around it.

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(300,300))

kernel = np.ones((5, 5), np.uint8)

# Opening Process
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

collage = cv2.hconcat([image,opening])
cv2.imshow("Original image --> Opening",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()