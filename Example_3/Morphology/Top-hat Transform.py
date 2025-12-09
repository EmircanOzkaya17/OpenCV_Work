import cv2
import numpy as np
# The formula is: Top-Hat = Original Image - Opening
# Amacı, resimdeki büyük nesneleri görmezden gelip, sadece küçük ve parlak (beyaz) detayları ortaya çıkarmaktır.

# Let's establish the logic step by step:
# Original Image: We have large white objects and small bright details next to them.

# What Happens If We Open?: Remember, the Opening process (Erosion + Dilation) erased the small white dots it considered noise, preserving the large objects.

# Subtraction (Difference): Now it's time for math:
# (Large Objects + Small Details) minus (Large Objects Only) = Small Details Only.

# In summary: the Top-Hat process erases the main body of the image (background and large objects), 
# leaving only those small bright parts that were lost during the Opening process.

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(300,300))

kernel = np.ones((9, 9), np.uint8)

# Result = Original - Opening(Original)
tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

collage = cv2.hconcat([image,tophat])
cv2.imshow("Original image --> Top-Hat",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()