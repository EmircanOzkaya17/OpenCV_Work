import cv2
import numpy as np
# The values ​​of the kernel matrix's central elements are high, and the values ​​decrease as you move away from the center.
# Example -->> [ [1, 2, 1] , [2, 4, 2] , [1, 2, 1] ]

# This allows the pixel in the center of the image to be multiplied by a larger factor.

# If the sum of the elements of the kernel matrix is ​​N, the kernel is multiplied by 1/N.

image =cv2.imread("swartz.jpg")
image=cv2.resize(image,(300,300))

g_blurring=cv2.GaussianBlur(image,(9,9),0) # (image, (kernel_width, kernel_height)
# We usually write 0 instead of sigmaX, in which case OpenCV says 
# "You wrote 0, but I will calculate the optimal standard deviation myself, looking at the kernel size."

collage=cv2.hconcat([image,g_blurring])

cv2.imshow("Gasussian Blurring",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()