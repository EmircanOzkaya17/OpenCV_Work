import cv2
import numpy as np
# Every pixel covered by the kernel is affected equally

image=cv2.imread("swartz.jpg")
image=cv2.resize(image,(300,300))
kernel = np.ones((5,5),np.float32)/25 # All elements of the matrix are 1. Multiplication coefficient of 25 matrices
#                                       This is a method to create a kernel

blurring_1=cv2.filter2D(image, -1, kernel)

# Or you can directly apply the process as follows

blurring_2=cv2.blur(image, (5,5))


collage=cv2.hconcat([image,blurring_1,blurring_2])

cv2.imshow("Average Blurring ", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()