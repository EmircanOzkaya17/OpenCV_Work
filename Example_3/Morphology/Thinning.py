import cv2
import numpy as np

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(500,500))

# Binarize
# For thinning, pixels must be clearly 0 (black) or 255 (white).
# Automatic matching is possible with the Otsu method.
ret,binary_img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Thinning generally works on white objects (255). 
# If your image has black text on a white background, you need to invert it:
# binary_img = cv2.bitwise_not(binary_img)

# Thinning Process
# We use the ximgproc module.
# The thinningType parameter selects the algorithm (ZHANGSUEN or GUOHALL)
thinning_result = cv2.ximgproc.thinning(binary_img, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

cv2.imshow('Orijinal Binary', binary_img)
cv2.imshow('Inceltme (Thinning) Sonucu', thinning_result)

cv2.waitKey(0)
cv2.destroyAllWindows()

