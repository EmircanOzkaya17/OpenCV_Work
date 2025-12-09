import cv2
import numpy as np
# It uses a mathematical process called convolution to make edges and details more distinct.
# The kernel increases the contrast between the central pixel and its neighbors by changing the values ​​of the pixels it overlays.

image=cv2.imread("swartz.jpg")
image=cv2.resize(image,(500,500))

kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
sharp_image = cv2.filter2D(image, -1, kernel)

collage=cv2.hconcat([image,sharp_image])

cv2.imshow("Kernel image",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()